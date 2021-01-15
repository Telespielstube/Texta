import threading, time

from Connection import Connection
from Configuration import Configuration
from RoutingTable import RoutingTable
from RouteRequest import RouteRequest
from RouteReply import RouteReply
from RouteError import RouteError
from RouteAcknowledge import RouteAcknowledge
from TextMessage import TextMessage
from UserMessage import UserMessage
from UserInterface import UserInterface

class Writer(threading.Thread):

    # Constructor for Writer class.
    # @connection       connection to the serial device
    # @header           
    # @configuration    
    def __init__(self, connection, configuration, routing_table):
        super(Writer,self).__init__()
        self.connection = connection
        self.configuration = configuration
        self.routing_table = routing_table
        self.pending_message_list = []
        self.ack_message_list = []
       # self.ticker = threading.Event()

    # Find a route to the request_message node
    # @request          Request message object.
    # @n
    def route_request(self, request, neighbor_node):
        if request.source == self.configuration.MY_ADDRESS and self.routing_table.search_entry(request.source):
            print('Request reached request source,')
            return
        if request.requested_node == self.configuration.MY_ADDRESS:
            print('Request reached end node')
            if not self.routing_table.search_entry(request.source):  
                self.routing_table.add_route_to_table(request.source, neighbor_node, request.hop)
                print('Route to source added')       
            self.send_message(message_to_string(RouteReply(request.source, 4, 9, 0, self.configuration.MY_ADDRESS, neighbor_node), b'0'))
        else:
            if not self.routing_table.search_entry(request.source): 
                self.routing_table.add_route_to_table(request.source, neighbor_node, request.hop)
            # do i have the requested node adress in table
            if self.routing_table.search_entry(request.requested_node):
                self.send_message(message_to_string(RouteReply(request.source, 4, 9, 0, request.requested_node, neighbor_node), b'0'))
            elif request.decrement_time_to_live() > 0:
                self.send_message(self.message_to_string(request, neighbor_node) )
                print('Request forwarded')
    
    # Sends a reply to the source node if own address matches request_messageed node.
    # RouteReply(source, destination, flag, time_to_live, previous_node, end_node, metric))
    # reply            Reply message object.
    # neighbor_node    Neighbor node address.
    def route_reply(self, reply, neighbor_node):
        if reply.end_node == self.configuration.MY_ADDRESS:
            print('Reply reached end node')
            self.routing_table.add_route_to_table(reply.source, neighbor_node, reply.hop)
        if reply.source == self.configuration.MY_ADDRESS:
            print('Reply reached reply sender.')            
        elif reply.next_node == self.configuration.MY_ADDRESS:
            if reply.time_to_live > 0:
                self.routing_table.add_route_to_table(reply.end_node, neighbor_node, reply.hop)
                reply.decrement_time_to_live(reply.time_to_live)
                self.send_message(self.message_to_string(reply, neighbor_node))
                print('Reply sent forwarded .')
    
    # Prepares the route message for sending. 
    # error    RouteError message object
    def route_error(self, error):
        if self.routing_table.find_route(error.broken_node, error.neighbor_node):
            self.routing_table.remove_route_from_table()
           
        self.send_message(self.message_to_string(error))
        print('Route Error forwarded')

    # Forwards the received message if destination is not own address.
    # text_message    TextMessage to be forwarded to next node.
    def forward_message(self, text_message):
        if text_message.next_node != self.configuration.MY_ADDRESS:
            if text_message.decrement_time_to_live(text_message.time_to_live) > 0:
                self.send_message(self.message_to_string(text_message))
                print('Text message forwarded.')
            else:
                self.route_error(RouteError(self.configuration.MY_ADDRESS, 5, 9, text_message.destination))
        else:
            UserInterface.print_message(text_message.source, text_message.payload)
    
    # Prepares the user text message for sending.
    # user_message    MessageItem object. Represents the user input.
    def text_message(self, user_message):
        self.send_message(self.message_to_string(user_message))
        print('Text message sent')

    # Message from the user interface
    # @user_message    text message        
    def user_input(self, user_message):
        best_route = self.routing_table.find_route(user_message.destination)
        if not best_route: # best route means the neighbor with the lowest costs to the destination. 
            self.send_message(RouteRequest(self.configuration.MY_ADDRESS, 3, 9, user_message.destination, 0), self.configuration.MY_ADDRESS)
            self.pending_message_list.append(user_message)
            print('Message is pending')
        else:
            self.text_message(TextMessage(self.configuration.MY_ADDRESS, 1, 9, user_message.destination, best_route, user_message.message))

    # Converts all different data types of the message to string and adds the field seperator.
    # @message    ields of the message  
    def message_to_string(self, message): 
        seperator = '|'
        separated_message = ''
        for attr, value in message.__dict__.items():
            if type(value) == bytes:
                value = value.decode()
            separated_message += str(value) + seperator
        return seperator + separated_message

    # Prepares the message for sending to the write_to_mcu function.
    # @message      holds all specific fields the message object has
    def send_message(self, message):
            self.connection.lock()
            command_string = 'AT+SEND='
            command_string += str(len(message))
            self.connection.write_to_mcu(command_string)
            print(self.connection.read_from_mcu())
            self.connection.write_to_mcu(message)
            print(self.connection.read_from_mcu())
            self.connection.unlock()

    # Overwritten thread run() function. Checks the list entries regularily for further processing of pending messages.
    def run(self): 
        while True:
            if not self.pending_message_list:
                message = UserMessage.get_pending_message_route(self.routing_table, self.pending_message_list)
                print(message)
                self.user_input(message)
                self.pending_message_list.remove(message)
                
            # if self.ticker.wait(Writer.CHECK_ACK_TABLE) and self.acknowledgment_list.destination is ack_message.source:
            #     remove_entry()
            # else:
            #     if ack hast arrived after 3 resents the the destination gets removed  
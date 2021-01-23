import threading, time 

from Connection import Connection
from Configuration import Configuration
from RoutingTable import RoutingTable
from PendingMessage import PendingMessage
from RouteRequest import RouteRequest
from RouteReply import RouteReply
from RouteError import RouteError
from RouteAck import RouteAck
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

    # Find a route to the request_message node
    # @request          Request message object.
    # @neigbor_node     previous node.
    def route_request(self, request, neighbor_node):
        if request.source == self.configuration.MY_ADDRESS and self.routing_table.search_entry(request.source):
            print('Request reached origin.')
        if request.requested_node == self.configuration.MY_ADDRESS:
            print('Request reached end node')
            if not self.routing_table.search_entry(request.source): 
                request.increment_hop() 
                self.routing_table.add_route_to_table(request.source, neighbor_node, request.hop)     
            self.send_message(self.message_to_string(RouteReply(self.configuration.MY_ADDRESS, 4, 9, 0, request.source, neighbor_node)))
        else:
            if not self.routing_table.search_entry(request.source):
                request.increment_hop() 
                self.routing_table.add_route_to_table(request.source, neighbor_node, request.hop)
            if self.routing_table.search_entry(request.requested_node):  
                self.send_message(self.message_to_string(RouteReply(request.source, 4, 9, 0, request.source, neighbor_node)))
            elif request.decrement_time_to_live() > 0:  
                request.increment_hop()
                self.send_message(self.message_to_string(request))
                print('Request forwarded')
            else:
                print('ttl = 0. Request deleted')
                pass
    
    # Sends a reply to the source node if own address matches request_messageed node.
    # RouteReply(source, destination, flag, time_to_live, previous_node, end_node, metric))
    # reply            Reply message object.
    # neighbor_node    Neighbor node address.
    def route_reply(self, reply, neighbor_node):
        if reply.source == self.configuration.MY_ADDRESS and self.routing_table.search_entry(reply.source):
            print('Reply reached origin.') 
            pass   
        if reply.end_node == self.configuration.MY_ADDRESS and reply.next_node == self.configuration.MY_ADDRESS:
            print('Reply reached end node')
            if not self.routing_table.search_entry(reply.source):  
                reply.increment_hop()
                self.routing_table.add_route_to_table(reply.source, neighbor_node, reply.hop)              
        if reply.next_node == self.configuration.MY_ADDRESS and not self.routing_table.search_entry(reply.source):
            reply.increment_hop()
            self.routing_table.add_route_to_table(reply.end_node, neighbor_node, reply.hop)
            if reply.decrement_time_to_live() > 0:              
                reply.increment_hop(reply.hop)    
                self.send_message(self.message_to_string(reply))
                print('Reply forwarded.')
            else: 
                print('ttl = 0 reply deleted')
                pass
        if reply.next_node != self.configuration.MY_ADDRESS:
            pass
           
    # Prepares the route message for sending. 
    # error    RouteError message object
    def route_error(self, error, neighbor_node):
        self.routing_table.remove_route_from_table(error.broken_node)          
        self.send_message(self.message_to_string(error))
        print('Route Error forwarded')

    # Forwards the received message if destination is not own address.
    # text_message    TextMessage to be forwarded to next node.
    def forward_message(self, text_message):
        if text_message.next_node == self.configuration.MY_ADDRESS and text_message.end_node != self.configuration.MY_ADDRESS:
            if text_message.decrement_time_to_live() > 0:
                self.send_message(self.message_to_string(text_message))
                print('Text message forwarded.')
               # self.ack_message_list.append(text_message) 
        else:
            pass  
        if text_message.destination == self.configuration.MY_ADDRESS and text_message.next_node == self.configuration.MY_ADDRERSS:
            UserInterface.print_message(text_message.source, text_message.payload.decode())

    # Prepares the user text message for sending.
    # user_message    MessageItem object. Represents the user input.
    def text_message(self, user_message):
        self.send_message(self.message_to_string(user_message))
        print('Text message sent')

    # Message from the user interface
    # @user_message    text message        
    def user_input(self, user_message):
        route = self.routing_table.find_route(user_message.destination)
        if not route:  
            self.send_message(self.message_to_string(RouteRequest(self.configuration.MY_ADDRESS, 3, 9, 0, user_message.destination))) 
            #Puts pendng message into a list.
            self.pending_message_list.append(PendingMessage(user_message, 1))
            print('Message is pending')
        else:
            self.text_message(TextMessage(self.configuration.MY_ADDRESS, 1, 9, user_message.destination, route, user_message.message))
            #self.ack_message_list(user_message)

    # Converts all different data types of the message to string and adds the field seperator.
    # @message    ields of the message  
    def message_to_string(self, message): 
        separator = '|'
        separated_message = ''
        for attr, value in message.__dict__.items():
            if type(value) == bytes:
                value = value.decode() 
            separated_message += str(value) + separator
        return separator + separated_message 

    # Prepares the message for sending to the write_to_mcu function.
    # @message      holds all specific fields the message object has
    def send_message(self, message):
            self.connection.lock()
            command_string = 'AT+SEND='
            command_string += str(len(message))
            self.connection.write_to_mcu(command_string)
            time.sleep(1)
            print(self.connection.read_from_mcu())
            self.connection.write_to_mcu(message)
            time.sleep(1)
            print(self.connection.read_from_mcu())
            self.connection.unlock()

    # Compares pending_message_list message destination and routing table destination esntry for matches.
    # @return     list with matching messages
    def get_pending_message_from_list(self):
        match = []
        for key in self.routing_table.table.keys():
            for entry in self.pending_message_list:
                if key is entry.message.destination:
                    match.append(entry.message.message)
        return match

    # Checks availablility of message destinations. If available they will be sent
    # otherwise retries will be counted up and the messages may be deleted. 
    def process_pending_user_message(self):
        matching_address = self.get_pending_message_from_list()   
        print(matching_address)  
        if matching_address:
            for entry in matching_address:    
                self.message_list.remove(entry) 
                self.user_input(entry) 
        else:
            pass

    # Thread function checks the list entries for further processing of pending messages and ack messages.
    def run(self): 
        while True:
            time.sleep(0.2)
                
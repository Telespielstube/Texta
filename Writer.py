import threading, time

from Connection import Connection
from Configuration import Configuration
from RoutingTable import RoutingTable
from MessageItem import MessageItem
from RouteRequest import RouteRequest
from RouteReply import RouteReply
from RouteError import RouteError
from RouteUnreachable import RouteUnreachable
from TextMessage import TextMessage
from UserInterface import UserInterface
from Route import Route

class Writer(threading.Thread):
    WAIT_TO_CHECK_TABLE_ENTRY = 5
    WAIT_TO_SEND_MESSAGE_AGAIN = 10
    CHECK_ACk_LIST = 8

    # Constructor for Writer class.
    # @connection       connection to the serial device
    # @header           
    # @configuration    
    def __init__(self, connection, configuration, routing_table):
        super(Writer,self).__init__()
        self.connection = connection
        self.configuration = configuration
        self.routing_table = routing_table
        self.pending_message_table = dict()
        self.ticker = threading.Event()
        self.pending_message_destination = ''
        self.user_message = MessageItem()
        self.best_route = Route()

    # Find a route to the request_message node
    # @request          Request message object.
    # @neighbor_node    Neighbor node address.
    def route_request(self, request, neighbor_node):
        if request.requested_node is self.routing_table.find_entry(request.requested_node):
            self.route_reply(RouteReply(self.configuration.MY_ADDRESS, 4, 9, 0, request.source, neighbor_node), b'0')
        elif request.source == self.configuration.MY_ADDRESS:
            pass
        else:
            if not self.routing_table.find_route_in_table(request, neighbor_node):
                request.hop = request.increment_hop() 
                self.routing_table.add_route_to_table(request.source, neighbor_node, request.hop) 
                time_to_live = request.decrement_time_to_live()
                if time_to_live > 0:
                    self.send_message(self.message_to_string(request, neighbor_node) )
                    print('Request forwarded')
                else:
                    self.route_unreachable(RouteUnreachable(self.configuration.MY_ADRESS, 6, 9, request.requested_node))
        if request.requested_node is self.configuration.MY_ADDRESS:
            print('Request reached end node')
            self.routing_table.add_route_to_table(request.source, neighbor_node, request.hop)
            self.route_reply(RouteReply(self.configuration.MY_ADDRESS, 4, 9, 0, request.source, neighbor_node))

    # Sends a reply to the source node if own address matches request_messageed node.
    # RouteReply(source, destination, flag, time_to_live, previous_node, end_node, metric))
    # reply            Reply message object.
    # neighbor_node    Neighbor node address.
    def route_reply(self, reply, neighbor_node):
        if reply.end_node != self.configuration.MY_ADDRESS:
            self.routing_table.add_route_to_table(reply.source, neighbor_node, reply.hop)
            time_to_live = reply.decrement_time_to_live()
            if time_to_live > 0:
                reply.hop = reply.increment_hop()
                self.send_message(self.message_to_string(reply, neighbor_node))
                print('Reply sent.')
            else:
                self.route_unreachable(RouteUnreachable(self.configuration.MY_ADRESS, 6, 9, reply.end_node))
        else:
            self.routing_table.add_route_to_table(reply.source, neighbor_node, reply.hop)

    # Prepares the route message for sending. 
    # error    RouteError message object
    def route_error(self, error):
        if self.routing_table.find_route_in_table(error.broken_node, error.neighbor_node):
            self.routing_table.remove_route_from_table()
            
        self.send_message(self.message_to_string(error))
        print('Route Error forwarded')

    # Prepares the message if the requested node is unreachable
    # unreachable  RouteUnreachable message object
    def route_unreachable(self, unreachable):
        self.send_message(self.message_to_string(unreachable))
        print('Route unreachable sent.')

    # Forwards the received message if destination is not own address.
    # text_message    TextMessage to be forwarded to next node.
    def forward_message(self, text_message):
        if text_message.next_node != self.configuration.MY_ADDRESS:
            time_to_live = text_message.decrement_time_to_live(text_message.time_to_live)
            if time_to_live != 0:
                self.send_message(self.message_to_string(text_message))
                print('Text message forwarded.')
            else:
                self.route_error(RouteError(self.configuration.MY_ADDRESS, 5, 9, text_message.destination))
        else:
            UserInterface.print_message(text_message.payload, text_message.source)
    
    # Prepares the user text message for sending.
    # user_message    MessageItem object. Represents the user input.
    def text_message(self, user_message):
        self.send_message(self.message_to_string(user_message))
        print('Text message sent. ')

    # Message from the user interface
    # @user_message    text message        
    def user_input(self, user_message):
        print('Writer:' + user_message.command + user_message.message + user_message.destination)       
        best_route = self.routing_table.find_best_route(user_message.destination)
        if not best_route: # best route means the neighbor with the lowest costs to the destination. :
            print(Route)
            self.route_request(RouteRequest(self.configuration.MY_ADDRESS, 3, 9, user_message.destination, 0), self.configuration.MY_ADDRESS)
            self.user_message = user_message
            self.pending_message_table[user_message.destination] = user_message
        else:
            self.text_message(TextMessage(self.configuration.MY_ADDRESS, 1, 9, user_message.destination, best_route.neighbor, user_message.message))

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
    
    # Converts all different data types of the message to a utf-8 string.
    # @arguments    all fields of the message
    def message_to_string(self, *arguments):
        message_as_string = ''
        for field in arguments:
            message_as_string += str(field) # it is probably not working. If so delete decode('utf-8')
        return message_as_string

    # Overwritten thread function.
    def run(self): 
        while True:
            if self.ticker.wait(Writer.WAIT_TO_CHECK_TABLE_ENTRY) and self.pending_message_table(self.pending_message_destination, self.user_message): 
                    self.user_input(self.user_message)
            else:
                pass
            # if self.ticker.wait(Writer.CHECK_ACK_TABLE) and self.acknowledgment_list.destination is ack_message.source:
            #     remove_entry()
            # else:
            #     if ack hast arrived after 3 resents the the destination gets deleted from 
            
            
            
            
            


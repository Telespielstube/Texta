import threading
from time import sleep

from Connection import Connection
from Configuration import Configuration
from RoutingTable import RoutingTable
from MessageItem import MessageItem
from RouteRequest import RouteRequest
from RouteReply import RouteReply
from RouteError import RouteError
from TextMessage import TextMessage
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
        self.build_message = ''
    
    # Find a route to the request_message node
    # @request          Request message object.
    # @neighbor_node    Neighbor node adress.
    def route_request(self, request, neighbor_node):
        if request.requested_node is self.routing_table.find_entry(request.requested_node):
            self.route_reply(RouteReply(self.configuration.MY_ADDRESS, 4, 9, request.hop, request.source, neighbor_node), b'0')
        elif request.source == self.configuration.MY_ADDRESS:
            pass
        else:
            request.hop = request.increment_hop(request.hop)
          #  print('Adding route entry ' + str(request.source) + repr(request.hop))
            self.routing_table.add_route_to_table(request.source, neighbor_node, request.hop) 
            time_to_live = request.decrement_time_to_live(request.time_to_live)
            if time_to_live != 0:
                request.hop = request.increment_hop(request.hop)
                self.build_message = self.message_to_string(request, neighbor_node) 
                self.send_message()
                print('Request forwarded')
            else:
                pass
        if request.requested_node is self.configuration.MY_ADDRESS:
            print('Request reached end node')
            self.routing_table.add_route_to_table(request.source, neighbor_node, request.hop)
            hop = request.increment_hop(0)
            self.route_reply(RouteReply(self.configuration.MY_ADDRESS, 4, 9, hop, request.source, neighbor_node))

    # Sends a reply to the source node if own address matches request_messageed node.
    # RouteReply(source, destination, flag, time_to_live, previous_node, end_node, metric))
    # reply            Reply message object.
    # neighbor_node    Neighbor node adress.
    def route_reply(self, reply, neighbor_node):
        if reply.end_node != self.configuration.MY_ADDRESS:
            time_to_live = reply.decrement_time_to_live(reply.time_to_live)
            if time_to_live != 0:
                reply.hop = reply.increment_hop(reply.hop)
                self.build_message = self.message_to_string(reply, neighbor_node)
                self.send_message()
                print('Reply sent.')
            else:
                pass
              #  self.route_error(RouteError(self.configuration.MY_ADDRESS, self.configuration.DESTINATION_ADDRESS, 5, 10, reply.end_node))
        else:
            self.routing_table.add_route_to_table(reply.source, neighbor_node, reply.hop)

    # Prepares the route message for sending. 
    # error    RouteError message object
    def route_error(self, error):
        self.build_message = self.message_to_string(error)
        self.send_message(self.build_message)
        print('Error forwarded')

    # Prepares the message if the requested node is unreachable
    # unreachable  RouteUnreachable message object
    def route_unreachable(self, unreachable):
        pass

    # Forwards the received message if destination is not own address.
    # text_message    TextMessage to be forwarded to next node.
    def forward_message(self, text_message):
        if text_message.next_node != self.configuration.MY_ADDRESS:
            time_to_live = text_message.decrement_time_to_live(text_message.time_to_live)
            if time_to_live != 0:
                self.build_message = self.message_to_string(text_message)
                self.send_message()
                print('Text message forwarded.')
            else:
                self.route_error(RouteError(self.configuration.MY_ADDRESS, 5, 10, text_message.destination))
        else:
            UserInterface.print_message(text_message.payload, text_message.source)
    
    # Prepares the user text message for sending.
    # user_message    MessageItem object. Represents the user input.
    def text_message(self, user_message):
        self.build_message = self.message_to_string(user_message)
        self.send_message()
        print('Text message sent. ')

    # Message from the user interface
    # @user_message    text message        
    def user_input_text_message(self, user_message):
        best_route = self.routing_table.find_best_route(user_message.destination) # best route means the neighbor with the lowest costs to the destination. 
        if not best_route:
            self.route_request(RouteRequest(self.configuration.MY_ADDRESS, 3, 10, user_message.destination, 0), self.configuration.MY_ADDRESS)
            # await route reply before sending out the message
        else:
            print(str(best_route))
            self.text_message(TextMessage(self.configuration.MY_ADDRESS, 1, 10, best_route, user_message.next_node, user_message.message))

    # Prepares the message for sending.
    # @message      holds all specific fields the message object has
    def send_message(self):
            self.connection.lock()
            print(self.build_message) # prints outgoing message
            command_string = 'AT+SEND='
            command_string += str(len(self.build_message))
            self.connection.write_to_mcu(command_string)
            print(self.connection.read_from_mcu())
            self.connection.write_to_mcu(self.build_message)
            print(self.connection.read_from_mcu())
            self.connection.unlock()
    
    # Converts all different data type of the message to a uniform string type
    # @arguments    all fields of the message
    def message_to_string(self, *arguments):
        message = ''
        for field in arguments:
            message += str(field)
        return message

    # Overwritten thread function.
    def run(self): 
        while True:
            if self.build_message != 0:
                sleep(0.2)
            else:
                sleep(0.2)


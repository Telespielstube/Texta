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
    def route_request(self, request, neighbor_node):
        if request.requested_node != self.configuration.MY_ADDRESS and self.routing_table.find_entry(request.requested_node != request.requested_node):
            self.routing_table.add_route_to_table(request.source, neighbor_node, request.metric) 
            time_to_live = request.decrement_time_to_live(request.time_to_live)
            if time_to_live != 0:
                metric = request.increment_metric(request.metric)
                self.build_message = self.message_to_string(request, neighbor_node) 
                self.send_message()
            else:
                pass
        if request.source is routing_table.find_entry(request.source):
            pass
        if request.requested_node == self.configuration.MY_ADDRESS:
            self.routing_table.add_route_to_table(request.source, neighbor_node, request.metric)
            self.route_reply(RouteReply(self.configuration.MY_ADDRESS, self.configuration.DESTINATION_ADDRESS, 4, 10, request.neighbor_node, request.source, 0))

    # Sends a reply to the source node if own address matches request_messageed node.
    # RouteReply(source, destination, flag, time_to_live, previous_node, end_node, metric))
    def route_reply(self, reply, neighbor_node):
        if reply.end_node != self.configuration.MY_ADDRESS:
            time_to_live = reply.decrement_time_to_live(reply.time_to_live)
            if time_to_live != 0:
                metric = reply.increment_metric(reply.metric)
                self.build_message = self.message_to_string(reply, neighbor_node)
                self.send_message()
            else:
                del reply
              #  self.route_error(RouteError(self.configuration.MY_ADDRESS, self.configuration.DESTINATION_ADDRESS, 5, 10, reply.end_node))
        else:
            self.routing_table.add_route_to_table(neighbor_node, reply.source, reply.metric)

    # Prepares the route message for sending. 
    def route_error(self, error):
        self.build_message = self.message_to_string(error)
        self.send_message(self.build_message)

    # Prepares the message if the requested node is unreachable
    # @unreachable  RouteUnreachable object
    def route_unreachable(self, unreachable):
        pass

    # Forwards the received message if destination is not own node address.
    def forward_message(self, text_message):
        if text_message.next_node != self.configuration.MY_ADDRESS:
            time_to_live = text_message.decrement_time_to_live(text_message.time_to_live)
            if time_to_live != 0:
                self.build_message = self.message_to_string(text_message)
                self.send_message()
            else:
                del text_message
                self.route_error(RouteError(self.configuration.MY_ADDRESS, self.configuration.DESTINATION_ADDRESS, 5, 10, ))
        else:
            UserInterface.print_message(text_message.payload)
    
    # Prepares the user text message for sending.
    def text_message(self, user_message):
        self.build_message = self.message_to_string(user_message)
        self.send_message()

    # Message from the user interface
    # @user_message    text message        
    def user_input_text_message(self, user_message):
        best_route = self.routing_table.find_best_route(user_message.destination) # best route means the neighbor with the lowest costs to the destination. 
        if not best_route:
            self.route_request(RouteRequest(self.configuration.MY_ADDRESS, self.configuration.DESTINATION_ADDRESS, 3, 10, user_message.destination, 0), self.configuration.MY_ADDRESS)
            # await route reply before sending out the message
        else:
            self.text_message(TextMessage(self.configuration.MY_ADDRESS, best_route, 1, 10,  user_message.next_node, user_message.message))

    # Prepares the message for sending.
    # @message      holds all specific fields the message object has
    def send_message(self):
            self.connection.lock()
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
        string_message = ''
        for field in arguments:
            string_message += str(field)
        return string_message

    # Overwritten thread function.
    def run(self): 
        while True:
            if self.build_message != 0:
                sleep(0.2)
            else:
                sleep(0.2)


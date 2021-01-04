import threading

from Connection import Connection
from Configuration import Configuration
from RoutingTable import RoutingTable
from MessageItem import MessageItem
from RouteRequest import RouteRequest
from RouteReply import RouteReply
from RouteError import RouteError
from TextMessage import TextMessage

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
        self.build_message = b''
    
    # Find a route to the request_messageed node
    def route_request(self, request):
        if request.requested_node != self.configuration.MY_ADDRESS:
            time_to_live = request.decrement_time_to_live(request.time_to_live)
            if time_to_live != 0:
                metric = request.increment_metric(request.metric)
                self.build_message = request.source + request.destination + request.flag + time_to_live + request.requested_node + metric
                self.send_message(self.build_message)
            else:
                del request
                self.route_error(RouteError(self.configuration.MY_ADDRESS, self.configuration.DESTINATION_ADDRESS, 5, 10, request.requested_node))
        else:
            self.routing_table.add_route_to_table(request.neighbor, request.source, request.metric)
            self.route_reply(RouteReply(self.configuration.MY_ADDRESS, self.configuration.DESTINATION_ADDRESS, 4, 10, request.neighbor_node, request.source, 0))

    # Sends a reply to the source node if own address matches request_messageed node.
    # RouteReply(source, destination, flag, time_to_live, previous_node, end_node, metric))
    def route_reply(self, reply):
        if reply.end_node != self.configuration.MY_ADDRESS:
            time_to_live = reply.decrement_time_to_live(reply.time_to_live)
            if time_to_live != 0:
                metric = reply.increment_metric(reply.metric)
                self.build_message = reply.source + reply.destination + reply.flag + time_to_live + reply.end_node + metric
                self.send_message(self.build_message)
            else:
                del reply
                self.route_error(RouteError(self.configuration.MY_ADDRESS, self.configuration.DESTINATION_ADDRESS, 5, 10, reply.end_node))
        else:
            self.routing_table.add_route_to_table(reply.neighbor, reply.source, reply.metric)

    # Prepares the route error object  
    def route_error(self, error):
        self.build_message = error.source + error.destination + error.flag + error.time_to_live + error.requested_node
        self.send_message(self.build_message)

    # Forwards the received message if destination is not own node address.
    def forward_message(self, text_message):
        pass

    # # Text message to a specific node.
    def text_message(self, text_message):
        if text_message.next_node != self.configuration.MY_ADDRESS:
            self.forward_message(text_message)
        else:
            self.build_message(text_message)

    # Prepares the different message object for sending.
    def process_message(self, message):
        if not self.routing_table.find_best_route(message.destination):
            self.route_request(RouteRequest(self.configuration.MY_ADDRESS, self.configuration.DESTINATION_ADDRESS, 3, 10, message.destination, 0))
        else:
            best_route = self.routing_table.find_best_route(message.destination)
            self.text_message(TextMessage(self.configuration.MY_ADDRESS, message.destination, 1, 10, best_route, message.message))
            self.build_message(message)

    # Prepares the message for sending.
    # @message      holds all specific fields the message object has
    def send_message(self, message):
        # if 'SEND' in message.command:
        #     self.connection.lock()
            # if message.destination:
            #     self.header.destination = message.destination
            #     command_string = 'AT+DEST=' + self.header.destination
            #     self.connection.write_to_mcu(command_string)
            #     print(self.connection.read_from_mcu())
            self.connection.lock()
            command_string = 'AT+SEND='
            command_string += len(str(message)) # convert and concatenate message length and command
            self.connection.write_to_mcu(command_string)
            print(self.connection.read_from_mcu())
            self.connection.write_to_mcu(message)
            print(self.connection.read_from_mcu())
            self.connection.unlock()
    
    def run(self): 
        while True:
            pass


import threading

from Connection import Connection
from Configuration import Configuration
from RoutingTable import RoutingTable
from MessageItem import MessageItem
from RouteRequest import RouteRequest
from RouteReply import RouteReply
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
    
    # Find a route to the request_messageed node
    def route_request(self, request_message):
        if request_message.request_messageed_node != self.configuration.MY_ADDRESS:
            RouteRequest.source = request_message.source
            RouteRequest.destination = request_message.destination
            RouteRequest.flag = request_message.flag
            RouteRequest.time_to_live = request_message.time_to_live - 1
            RouteRequest.requested_node = request_message.requested_node
            RouteRequest.metric = request_message.metric
           # self.build_message()
        #else:
           # self.route_reply(RouteReply(self.configuration.MY_ADDRESS, self.configuration.DESTINATION_ADDRESS, 4, 10, request_message.neighbor_node, request_message.source, 0))

    # Sends a reply to the source node if own address matches request_messageed node.
    # def route_reply(self, reply_message):
    #     if 

    # Forwards the received message if destination is not own node address.
    def forward_message(self, text_message):
        pass

    # # Text message to a specific node.
    def text_message(self, text_message):
        if text_message.next_node != self.configuration.MY_ADDRESS:
            self.forward_message(text_message)
        else:
            self.build_message(text_message)

    def process_message(self, message_body):
        if not self.routing_table.find_entry(message_body.destination):
            self.route_request(RouteRequest(self.configuration.MY_ADDRESS, self.configuration.DESTINATION_ADDRESS, 3, 10, message_body.destination, 0))
        else:
            best_route = self.routing_table.select_best_route()
            self.text_message(TextMessage(self.configuration.MY_ADDRESS, message_body.destination, 1, 10, best_route, message_body.message))
            self.build_message(message_body)

    # Prepares the message for sending.
    # @self function is a member of this object
    def build_message(self, *message_body):
        # if 'SEND' in message_body.command:
        #     self.connection.lock()
            # if message_body.destination:
            #     self.header.destination = message_body.destination
            #     command_string = 'AT+DEST=' + self.header.destination
            #     self.connection.write_to_mcu(command_string)
            #     print(self.connection.read_from_mcu())
            self.connection.lock()
            command_string = 'AT+SEND='
            payload = len(message_body)
            payload_length = 0
            payload_length += len(payload) + 10 # MCU header length
            command_string += str(payload_length) # concatenate message length and command
            self.connection.write_to_mcu(command_string)
            print(self.connection.read_from_mcu())
            message = b''
            for field in message_body:
                message += field
            self.connection.write_to_mcu(message)
            print(self.connection.read_from_mcu())
            self.connection.unlock()
    
    def run(self): 
        while True:
            self.build_message()  

                


            

            
            



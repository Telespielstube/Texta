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
    def route_request(self, request):
        if request.requested_node != self.configuration.MY_ADDRESS:
            time_to_live = request.decrement_time_to_live(request.time_to_live)
            if time_to_live != 0:
                metric = request.increment_metric(request.metric)
                build_request = request.source + request.destination + request.flag + time_to_live + request.requested_node + metric
                self.send_message(build_request)
            else:
                del request
                #self.route_error(RouteError())
        else:
            # add adress to table
            self.route_reply(RouteReply(self.configuration.MY_ADDRESS, self.configuration.DESTINATION_ADDRESS, 4, 10, request.neighbor_node, request.source, 0))

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
    def send_message(self, message):
        # if 'SEND' in message_body.command:
        #     self.connection.lock()
            # if message_body.destination:
            #     self.header.destination = message_body.destination
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
 

                


            

            
            



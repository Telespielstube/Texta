import threading

from Connection import Connection
from Configuration import Configuration
from MessageHeader import MessageHeader
from MessageItem import MessageItem
from RouteRequest import RouteRequest
from RouteReply import RouteReply
from TextMessage import TextMessage

class Writer(threading.Thread):
    
    # Constructor for Writer class.
    # @connection       connection to the serial device
    # @header           
    # @configuration    
    def __init__(self, connection, header, configuration, routing_table):
        super(Writer,self).__init__()
        self.connection = connection
        self.header = header
        self.configuration = configuration
        self.routing_table = routing_table
    
    # Find a route to the requested node
    def route_request(self, request):
        if request.requested_node != self.configuration.MY_ADDRESS:
            MessageHeader.source = request.source
            MessageHeader.destination = request.destination

           #set header fields and build message   

    # Sends a reply to the source node if own address matches requested node.
    # def route_reply(self):
    #     if 

    # Forwards the received message if destination is not own node address.
    #def forward_message(self, text_message):

    # Text message to a specific node.
    def text_message(self, text_message):
        if text_message.next_node is not self.configuration.MY_ADDRESS:
            self.forward_message(text_message)
        else:
            pass

    def message_processor(self, message_item):
        if not self.routing_table.find_entry(message_item.destination):
            self.route_request(message_item)
        else:
            #best_route = self.routing_table
            self.message_builder(message_item)

    # Prepares the message for sending.
    # @self function is a member of this object
    def message_builder(self, message_item):
        if 'SEND' in message_item.command:
            self.connection.lock()
            # if message_item.destination:
            #     self.header.destination = message_item.destination
            #     command_string = 'AT+DEST=' + self.header.destination
            #     self.connection.write_to_mcu(command_string)
            #     print(self.connection.read_from_mcu())
            command_string = 'AT+SEND='
            payload = message_item.message
            payload_length = 0
            payload_length += len(payload) + 10
            command_string += str(payload_length)
            self.connection.write_to_mcu(command_string)
            print(self.connection.read_from_mcu())
            self.check_header_flag()
            message = (self.header.build_header(self.configuration.MY_ADDRESS) + payload)
            self.connection.write_to_mcu(message)
            print(self.connection.read_from_mcu())
            self.connection.unlock()
    
    def run(self): 
        while True:
            self.message_builder()  

                


            

            
            



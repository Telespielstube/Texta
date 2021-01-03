import threading

from Connection import Connection
from Header import Header
from Configuration import Configuration
from MessageItem import MessageItem
from RouteRequest import RouteRequest
from RouteReply import RouteReply
from TextMessage import TextMessage

class Writer(threading.Thread):
    
    # Constructor for Writer class.
    # @connection       connection to the serial device
    # @header           
    # @configuration    
    def __init__(self, connection, header, configuration):
        super(Writer,self).__init__()
        self.connection = connection
        self.header = header
        self.configuration = configuration
    
    # Find a route to the requested node
    def route_request(self, request_message):
        if request_message.requested_node != self.configuraton.MY_ADDRESS:


    # Sends a reply to the source node if own address matches requested node.
    # def route_reply(self):
    #     if 

    # Forwards the received message if destination is not own node address.
    # def forward_message(self):

    # Prepares the message for sending.
    # @self function is a member of this object
    # def message_builder(self, message_item):
    #     if 'SEND' in message_item.command:
    #         self.connection.lock()
    #         # if message_item.destination:
    #         #     self.header.destination = message_item.destination
    #         #     command_string = 'AT+DEST=' + self.header.destination
    #         #     self.connection.write_to_mcu(command_string)
    #         #     print(self.connection.read_from_mcu())
    #         command_string = 'AT+SEND='
    #         payload = message_item.message
    #         payload_length = 0
    #         payload_length += len(payload) + 10
    #         command_string += str(payload_length)
    #         self.connection.write_to_mcu(command_string)
    #         print(self.connection.read_from_mcu())
    #         self.check_header_flag()
    #         message = (self.header.build_header(self.configuration.MY_ADDRESS) + payload)
    #         self.connection.write_to_mcu(message)
    #         print(self.connection.read_from_mcu())
    #         self.connection.unlock()
    #     self.transmit_queue.task_done()
    
    def run(self): 
        while True:
            self.message_builder()  

                


            

            
            



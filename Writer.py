import threading
import time

from Connection import Connection
from Header import Header
from MessageItem import MessageItem

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

    def check_header_flag(self):
        if self.header.flag != 0 and self.header.flag != 2 and self.header.flag != 3 and self.header.flag != 4 and self.header.flag != 5:
            self.header.flag = 1
    
    # Forwards the received message if destination is not own node address.
    # def forward_message(self):

    # Find a rout to the requested node
    def route_request(self):

    # Sends a reply to the source node if own address matches requested node.
    # def route_reply(self):
    #     if 

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
            if self.transmit_queue.empty():
                time.sleep(0.5)
            while not self.transmit_queue.empty():
                self.message_builder()  

                


            

            
            



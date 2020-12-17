import threading
import queue
import time

from Connection import Connection
from Header import Header
from MessageItem import MessageItem

class Writer(threading.Thread):
    MY_ADDRESS = '0136'

    # Constructor for Writer class.
    # @thread_id        thread id
    # @name             thread name
    # @connection       connection to the serial device
    # @trasmit_queue    initializes thread safe queu Object
    # @header           initializes Header Object 
    def __init__(self, thread_id, name, connection):
        super(Writer,self).__init__()
        self.thread_id = thread_id
        self.name = name
        self.communicate = connection
        self.transmit_queue = queue.Queue()
        self.header = Header()
    
    # Prepares the message for sending.
    # @self function is a member of this object. 
    def message_builder(self):
        message_item = self.transmit_queue.get()
        if 'SEND' in message_item.command:
            if message_item.destination:
                destination_address = message_item.destination
                command_string = 'AT+DEST=' + destination_address
                self.communicate.write_to_mcu(command_string)
                self.communicate.read_from_mcu()
            command_string = 'AT+SEND='
            payload = message_item.message
            payload_length = 0
            payload_length += len(payload) + 10
            command_string += str(payload_length)
            self.communicate.write_to_mcu(command_string)
            time.sleep(1)
            message = self.header.build_header(Writer.MY_ADDRESS, destination_address) + payload + '\r\n'
        self.communicate.write_to_mcu(message)
        self.communicate.read_from_mcu()
        time.sleep(0.5)
        self.transmit_queue.task_done()

    def run(self): 
        while True:
            if self.transmit_queue.empty():
                time.sleep(0.5)
            while not self.transmit_queue.empty():
                self.message_builder()  

                


            

            
            



import threading
import time

from Connection import Connection
from Parser import Parser
class Reader(threading.Thread):

    # Constructor for Reader class.
    # @connection   connection to the serial device
    # @parser       Parser for incoming messages
    def __init__(self, connection, parser):
        super(Reader, self).__init__()
        self.connection = connection
        self.parser = parser
            
    # Prints received data on screen.
    # @message    received data encoded to utf-8
    def print_received_message(self, message):
        print(message[:-1].decode())

    # Overridden Thread function to execute functions necessary to read from mcu.
    def run(self):
        # constantly read from mcu, if received message is empty 
        # sleep if message has content break from if statement and put message to queue
        while True:
            self.connection.lock()
            message = self.connection.read_from_mcu()
            self.connection.unlock()
            if not message:
                time.sleep(0.2)
                continue
            self.parser.parse_incoming_message(message[:11], message[11:]) # slices incoming message in mcu and protcol part return vales are parsed.


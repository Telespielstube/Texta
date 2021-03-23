import threading, time

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

    def run(self):
        # constantly read from mcu, if received message is empty 
        # sleep if message has content break from if statement and pass message to parser
        while True:
            self.connection.lock()
            message = self.connection.read_from_mcu()
            self.connection.unlock()
            if not message:
                time.sleep(0.2)
                continue
            print('Reader: ' + message.decode())
            self.parser.parse_message(message[:11], message[11:]) #first message arg = MCU header, second is protocol header

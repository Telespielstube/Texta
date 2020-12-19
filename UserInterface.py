import threading
import queue
import sys

from Connection import Connection
from MessageItem import MessageItem
from RoutingTable import RoutingTable

class UserInterface(threading.Thread):

    # Constructor for Reader class.
    def __init__(self, communication, writer, reader, automator, routing_table):
        super(UserInterface,self).__init__()
        self.connection = communication
        self.writer = writer
        self.reader = reader
        self.automator = automator
        self.routing_table = routing_table
        
    def read_console_input(self):
        command = input()
        return command

    def select_option(self, option):
        command = option[:4] 
        message = option[5:-5] 
        destination = option[-4:] 
        if 'SEND' in command:
            message_item = MessageItem(command, message, destination)
            self.writer.transmit_queue.put(message_item)
        if 'ROUT' in command:
            print ('Routing Table')
            self.routing_table.show_routing_table()
        if 'EXIT' in command:
            self.writer.join()
            self.reader.join()
            self.automator.join()
            UserInterface.join()
            sys.exit(0)
            
    def run(self):
        while True:
            command = self.read_console_input()
            self.select_option(command)




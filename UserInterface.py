import threading, sys

from Connection import Connection
from UserMessage import UserMessage
from RoutingTable import RoutingTable

class UserInterface(threading.Thread):

    # Constructor for Reader class.
    def __init__(self, communication, writer, reader, routing_table):
        super(UserInterface,self).__init__()
        self.connection = communication
        self.writer = writer
        self.reader = reader
        self.routing_table = routing_table

    # reads user input.    
    def read_console_input(self):
        command = input()
        return command

    # Prints received data on screen.
    # @message    text message payload decoded to utf-8
    @staticmethod
    def print_message(source, payload):
        print('[' + source.decode() + '-->]   ' + payload.decode())

    def print_routing_table(self):
        print('Routing Table')
        print('---------------------------')
        print('| Source | Neighbor | hop |')
        print('---------------------------')
        self.routing_table.show_routing_table()

    # Minimalistic menu to navigate though the chat application. 
    def select_option(self, option):
        command = option[:4] 
        message = option[5:-5] 
        destination = option[-4:] 
        if 'SEND' in command:
            user_message = UserMessage(command, message, destination)
            self.writer.user_input(user_message)
        if 'USER' in command:
            self.print_routing_table()
        if 'EXIT' in command:
            self.writer.join()
            self.reader.join()
            UserInterface.join()
            sys.exit(0)
            
    def run(self):
        while True:
            command = self.read_console_input()
            self.select_option(command)




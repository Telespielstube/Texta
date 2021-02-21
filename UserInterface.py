import threading, sys

from Connection import Connection
from UserMessage import UserMessage
from RoutingTable import RoutingTable

class UserInterface(threading.Thread):

    # Constructor for Reader class.
    def __init__(self, communication, message_handler, reader, routing_table):
        super(UserInterface,self).__init__()
        self.connection = communication
        self.message_handler = message_handler
        self.reader = reader
        self.routing_table = routing_table

    # Prints received message on screen.
    # @message    text message payload decoded to utf-8
    @staticmethod
    def print_incoming_message(source, payload):
        print('[ ' + source.decode() + ' --> ]   ' + payload)

    # Prints outgoing message on screen.
    # @message    text message payload 
    @staticmethod
    def print_outgoing_message(destination, payload):
        print('[ ' + destination + ' <-- ]   ' + payload)

    # reads user input.    
    def read_console_input(self):
        command = input()
        return command

    # Print a formatted easy to read  version of the current routing table.     
    def print_routing_table(self):
        print('Routing Table')
        print('---------------------------')
        print('|  Dest  | Neighbor | hop |')
        print('---------------------------')
        self.routing_table.show_routing_table()

    # Minimalistic menu to navigate though the chat application. 
    # @option            option the user can choose from. 
    def select_option(self, option):
        if option[:4] == 'SEND' and option[-4:].isdigit():
            self.message_handler.user_input(UserMessage(option[5:-5], option[-4:]))
        elif option[:4] == 'USER':
            self.print_routing_table()
        else:
            print("Command incorrect. Try:\n"
            "SEND [your text (max. 244 characers, except '|' are not allowed)] [Adressformat: 1234]\nor:\n"
            "USER for displaying your routing table.")

    def run(self):
        while True:
            command = self.read_console_input()
            self.select_option(command)




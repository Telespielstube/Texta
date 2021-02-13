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
        print('[ ' + source.decode() + ' --> ]   ' + payload.decode())

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
        print('| Source | Neighbor | hop |')
        print('---------------------------')
        self.routing_table.show_routing_table()

    # Minimalistic menu to navigate though the chat application. 
    # @option            option the user can choose from. 
    def select_option(self, option):
        command = option[:4] 
        message = option[5:-5] 
        destination = option[-4:] 

        if 'SEND' in command and destination.isdigit():
            user_message = UserMessage(message, destination)
            self.message_handler.user_input(user_message)
        else:
            print("Message format incorrect. Correct format: SEND [your text (max. 244 characers)] [Adressformat: xxxx]")
        if 'USER' in command:
            self.print_routing_table()
        if 'EXIT' in command:
            self.connection.close_connection()
            sys.exit(0)
            
    def run(self):
        while True:
            command = self.read_console_input()
            self.select_option(command)




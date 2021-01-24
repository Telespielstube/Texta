import threading, sys

from Connection import Connection
from Configuration import Configuration    
from Writer import Writer
from Reader import Reader
from Parser import Parser
from PendingMessageHandler import PendingMessageHandler
from MessageHandler import MessageHandler
from UserInterface import UserInterface
from RoutingTable import RoutingTable

def main(argv):
    MY_ADDRESS = sys.argv  
    #connection = Connection('/dev/ttyS0', 115200, 8, 'N', 1, 5)
    connection = Connection('/dev/ttys003', 115200, 8, 'N', 1, 5)
    connection.connect_device()
    configuration = Configuration(connection, sys.argv[1])
    configuration.config_module('AT+RST', 'AT+CFG=433500000,5,9,7,1,1,0,0,0,0,3000,8,4', 'AT+ADDR=' + MY_ADDRESS, 'AT+DEST=FFFF', 'AT+RX', 'AT+SAVE')
    routing_table = RoutingTable(MY_ADDRESS.encode(), 0) #Adds own address and 0 hops to routing table
    writer = Writer(connection)
    message_handler = MessageHandler(MY_ADDRESS.encode(), routing_table, writer)
    parser = Parser(routing_table, message_handler)
    reader = Reader(connection, parser)  
    user_interface = UserInterface(connection, message_handler, reader, routing_table)
    pending_message_handler = PendingMessageHandler(message_handler)
    reader.start()
    user_interface.start()
    pending_message_handler.start()

if __name__ == '__main__':
    main(sys.argv)


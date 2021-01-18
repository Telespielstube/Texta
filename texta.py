import threading

from Connection import Connection
from Configuration import Configuration    
from Writer import Writer
from Reader import Reader
from Parser import Parser
from UserInterface import UserInterface
from RoutingTable import RoutingTable

def main():   
    connection = Connection('/dev/ttyS0', 115200, 8, 'N', 1, 5)
    #connection = Connection('/dev/ttys004', 115200, 8, 'N', 1, 5)
    connection.connect_device()
    configuration = Configuration(connection)
    configuration.config_module('AT+RST', 
                             'AT+CFG=433500000,5,6,12,1,1,0,0,0,0,3000,8,4', 
                             'AT+ADDR=0136',
                             'AT+DEST=FFFF',
                             'AT+RX',
                             'AT+SAVE')
    routing_table = RoutingTable(configuration.MY_ADDRESS, 0) #Adds own address and 0 hops to routing table
    writer = Writer(connection, configuration, routing_table)
    parser = Parser(routing_table, writer)
    reader = Reader(connection, parser)
    user_interface = UserInterface(connection, writer, reader, routing_table)
    writer.start()
    reader.start()
    user_interface.start()

if __name__ == '__main__':
    main()


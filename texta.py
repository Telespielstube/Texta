import threading

from Connection import Connection
from Configuration import Configuration    
from Writer import Writer
from Reader import Reader
from Parser import Parser
from UserInterface import UserInterface
from Automator import Automator
from RoutingTable import RoutingTable

def main():
   # Connecting and configure LoRa mcu.
   # connection = Connection('/dev/ttyS0', 115200, 8, 'N', 1, 5)
    connection = Connection('/dev/ttys003', 115200, 8, 'N', 1, 3)
    connection.connect_device()
    configure = Configuration(connection)
    configure.config_module('AT+RST', 'AT+CFG=433500000,20,6,12,1,1,0,0,0,0,3000,8,4', 
                            'AT+ADDR=0136',
                            'AT+DEST=FFFF',
                            'AT+RX',
                            'AT+SAVE')
    routing_table = RoutingTable()
    parser = Parser(routing_table)

    #Set up and start threads
    writer = Writer(1, 'writer', connection)
    reader = Reader(2, 'reader', connection, parser)
    user_interface = UserInterface(3, 'keyboard', connection, writer, routing_table)
    automator = Automator(4, 'automator', writer)
    writer.start()
    reader.start()
    user_interface.start()
    automator.start()

if __name__ == '__main__':
    main()


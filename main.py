import threading, time, argparse

from Connection import Connection
from Configuration import Configuration    
from Writer import Writer
from Reader import Reader
from Parser import Parser
from PendingMessageTimer import PendingMessageTimer
from MessageHandler import MessageHandler
from UserInterface import UserInterface
from RoutingTable import RoutingTable

def process_argument():
    parser = argparse.ArgumentParser(description='Add a valid address.')
    parser.add_argument('string', metavar='address', type=str, help='LoRa module address range from 0130 - 0140.')
    argv = parser.parse_args() 
    return argv.string

def main():
    MY_ADDRESS = process_argument()
    print('Minimalistic chat application that uses a LoRa modul for communication.\nType \'SEND\' to send a text(max. 240 Characters) or type \'USER\' to get an overview of all available chat peers.')
    time.sleep(5)
    connection = Connection('/dev/ttyS0', 115200, 8, 'N', 1, 6)
    #connection = Connection('/dev/ttys005', 115200, 8, 'N', 1, 5)
    connection.connect_device() 
    configuration = Configuration(connection)
    configuration.config_module('AT+RST', 'AT+CFG=433500000,5,9,7,1,1,0,0,0,0,3000,8,4', 'AT+ADDR=' + MY_ADDRESS, 'AT+DEST=FFFF', 'AT+RX', 'AT+SAVE')
    routing_table = RoutingTable(MY_ADDRESS.encode(), 0) #Adds own address and 0 hops to routing table
    writer = Writer(connection)
    message_handler = MessageHandler(MY_ADDRESS.encode(), routing_table, writer)
    pending_message_timer = PendingMessageTimer(message_handler)
    parser = Parser(routing_table, message_handler)
    reader = Reader(connection, parser)  
    user_interface = UserInterface(connection, message_handler, reader, routing_table)
    reader.start()
    user_interface.start()
    pending_message_timer.start()

if __name__ == '__main__':
    main()


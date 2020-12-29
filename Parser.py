from RoutingTable import RoutingTable
from Header import Header
from MessageItem import MessageItem
class Parser():

    def __init__(self, routing_table, header, writer, configuration):
        self.routing_table = routing_table
        self.header = header
        self.writer = writer
        self.configuration = configuration
    
    # flag 3 = Route Request, flag 4 = route reply, flag 5 = Route Error
    def parse_header_flag(self, flag):
        if flag == 3 and self.header.destination == self.configuration.MY_ADDRESS:
            self.routing_table.add_address_to_table(self.header.source)
        #if flag == 3 and self.header.destination != self.configuration.MY_ADDRESS:

            
    # Parsers the header of the incoming message.
    # @protocol_header    contains the header + payload as string. 
    def parse_protocol_header(self, protocol_header):       
        self.header.source = protocol_header[:4]#set the sliced source adress as source adress in header class
        self.header.destination = protocol_header[4:8]
        self.header.flag = protocol_header[8:9] # self.header.flag setter call in Python    
        self.header.time_to_live = protocol_header[9:10]
        self.parse_header_flag(self.header.flag)

    # Parses incoming byte stream. 
    # @line         the incoming message received by the LoRa mcu.
    # @transport    serial communication channel to the mcu.
    def parse_incoming_message(self, mcu_header, protocol_header):
        splitted = mcu_header.decode().split(',')
        if splitted[0] == 'AT' and splitted[1] == 'OK' or splitted[0] == 'ERR: PARA' or splitted[0] == 'ERR: CMD' or splitted[0] == 'CPU: BUSY':
            pass
        if splitted[0] == 'LR':
            self.parse_protocol_header(protocol_header)
    
    # Parses outgoing message.
    def parse_outgoing_message(self, message_item):
        requested_destination = message_item.destination
        if not self.routing_table.find_entry(requested_destination):
            
            self.writer.route_request()
        else:


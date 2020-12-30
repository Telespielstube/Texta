from RoutingTable import RoutingTable
from RouteRequest import RouteRequest
from RouteReply import RouteReply
class Parser():

    def __init__(self, routing_table, header, writer, configuration):
        self.routing_table = routing_table
        self.header = header
        self.writer = writer
        self.configuration = configuration
    
    # Based on the flag, the different fields are passed into the appropriate object. 
    def parse_header_flag(self, source, destination, flag, time_to_live, protocol_header, neighbor_node):
        if flag == b'3':
            requested_node = protocol_header[10:14] 
            metric = protocol_header[14:15]
            route_request = RouteRequest(source, destination, flag, time_to_live, requested_node, metric)
            self.writer.route_request(route_request)
        if flag == b'4':
            previous_node = protocol_header[10:14]
            end_node = protocol_header[14:18]
            metric = protocol_header[18:19]
            route_reply = RouteReply(source, destination, flag, time_to_live, previous_node, end_node, metric)
            self.writer.route_reply(route_reply)
        #if flag == b'5': 
        #if flag == b'1':

    # Parsers the header of the incoming message.
    # @protocol_header    contains the protocol message header. 
    # @neighbor_node      previous node that forwarded the message.
    def parse_protocol_header(self, protocol_header, neighbor_node):                   
        source = protocol_header[:4]#sets source adress
        destination = protocol_header[4:8]
        flag = protocol_header[8:9]
        time_to_live = protocol_header[9:10]
        self.parse_header_flag(source, destination, flag, time_to_live, protocol_header, neighbor_node) 

    # Parses incoming byte stream. 
    # @mcu_header   mcu message part.
    # @protocol_header protocol message part.
    def parse_incoming_message(self, mcu_header, protocol_header):
        splitted_header = mcu_header[:]
        if splitted_header[0] == 'LR':
            neighbor_node = b'splitted_header[1]'
            self.parse_protocol_header(protocol_header, neighbor_node)
        else:
            pass


from RoutingTable import RoutingTable
from RouteRequest import RouteRequest
from RouteReply import RouteReply
from RouteError import RouteError
from RouteUnreachable import RouteUnreachable
from TextMessage import TextMessage
class Parser():

    def __init__(self, routing_table, writer):
        self.routing_table = routing_table
        self.writer = writer
    
    # Based on the flag, the different fields are passed to the appropriate object. 
    # 1 = Textmassage, 3 = Request, 4 = Reply, 5 = Error, 6 = Node unreachable
    def parse_header_flag(self, source, flag, time_to_live, protocol_header, neighbor_node):
        if flag == b'1':
            destination = protocol_header[6:10]
            next_node = protocol_header[10:14]
            payload = protocol_header[14:]
            self.writer.forward_message(TextMessage(source, flag, time_to_live, destination, next_node, payload))
        if flag == b'3':
            hop = int.from_bytes(protocol_header[6:7], 'big')
            print(int(hop, base=10))
            requested_node = protocol_header[7:11]
            self.writer.route_request(RouteRequest(source, flag, time_to_live, hop, requested_node), neighbor_node)
        if flag == b'4':
            hop = int.from_bytes(protocol_header[17:18], 'big')
            end_node = protocol_header[18:22]
            next_node = protocol_header[22:]
            self.writer.route_reply(RouteReply(source, flag, time_to_live, hop, end_node, next_node), neighbor_node)
        if flag == b'5':
            broken_node = protocol_header[17:21]
            self.writer.route_error(RouteError(source, flag, time_to_live, broken_node))
        if flag == b'6':
            unreachable_node = protocol_header[17:21]
            self.writer.route_unreachable(RouteUnreachable(source, flag, time_to_live, unreachable_node))

    # Parsers the header of the incoming message.
    # @protocol_header    contains the protocol message header. 
    # @neighbor_node      previous node that forwarded the message.
    def parse_protocol_header(self, protocol_header, neighbor_node):                   
        source = protocol_header[:4]
        flag = protocol_header[4:5]
        time_to_live = int.from_bytes(protocol_header[5:6], 'big')
        self.parse_header_flag(source, flag, time_to_live, protocol_header, neighbor_node) 

    # Parses incoming byte stream. 
    # @mcu_header       mcu message part.
    # @protocol_header  protocol message part.
    def parse_incoming_message(self, mcu_header, protocol_header):
        neighbor_node = mcu_header[3:7]
        if mcu_header[:2] == b'LR':
            self.parse_protocol_header(protocol_header, neighbor_node)
        else:
            pass


from RoutingTable import RoutingTable
from RouteRequest import RouteRequest
from RouteReply import RouteReply
from RouteError import RouteError
from TextMessage import TextMessage
from RouteAcknowledgement import RouteAcknowledgement

class Parser():

    def __init__(self, routing_table, writer):
        self.routing_table = routing_table
        self.writer = writer
    
    # Based on the flag, the different fields are passed to the appropriate object. 
    # 1 = Textmassage, 3 = Request, 4 = Reply, 5 = Error, 6 = Node unreachable
    # field[0] = source adress, field[1] = flag, field [2] = ttl
    def parse_header(self, protocol_header, neighbor_node):
        protocol_field = protocol_header.split(b'|')
        if protocol_field[2] == b'1':
            self.writer.forward_message(TextMessage(protocol_field[1], protocol_field[2], protocol_field[3], protocol_field[4], protocol_field[5], protocol_field[6]))
        if protocol_field[2] == b'2':
            self.writer.acknowledgment_message(RouteAcknowledgement(protocol_field[1], protocol_field[2], protocol_field[3], int(protocol_field[4].decode()), protocol_field[5]))
        if protocol_field[2] == b'3':           
            self.writer.route_request(RouteRequest(protocol_field[1], protocol_field[2], protocol_field[3], int(protocol_field[4].decode()), protocol_field[5]), neighbor_node)
        if protocol_field[2] == b'4':
            self.writer.route_reply(RouteReply(protocol_field[1], protocol_field[2], protocol_field[3], int(protocol_field[4].decode()), protocol_field[5], protocol_field[6]), neighbor_node)
        if protocol_field[2] == b'5':
            self.writer.route_error(RouteError(protocol_field[1], protocol_field[2], protocol_field[3], protocol_field[4]), neighbor_node)

    # Parses incoming byte stream. 
    # @mcu_header       mcu message part.
    # @protocol_header  protocol message part.
    def parse_incoming_message(self, mcu_header, protocol_header):
        mcu_field = mcu_header.split(b',')
        if mcu_field[0] == b'LR':
            self.parse_header(protocol_header, mcu_field[1])
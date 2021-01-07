from RoutingTable import RoutingTable
from RouteRequest import RouteRequest
from RouteReply import RouteReply
from RouteError import RouteError
from TextMessage import TextMessage
class Parser():

    def __init__(self, routing_table, writer):
        self.routing_table = routing_table
        self.writer = writer
    
    # Based on the flag, the different fields are passed to the appropriate object. 
    # 1 = Textmassage
    # 3 = Request
    # 4 = Reply
    # 5 = Error
    # 6 = Node unreachable
    def parse_header_flag(self, source, destination, flag, time_to_live, protocol_header, neighbor_node):
        if flag == b'1':
            next_node = protocol_header[10:14]
            payload = protocol_header[14:]
            self.writer.forward_message(TextMessage(source, destination, flag, time_to_live, next_node, payload))
        if flag == b'3':
            requested_node = protocol_header[10:14] 
            metric = protocol_header[14:15]
            self.writer.route_request(RouteRequest(source, destination, flag, time_to_live, requested_node, metric), neighbor_node)
        if flag == b'4':
            previous_node = protocol_header[10:14]
            end_node = protocol_header[14:18]
            metric = protocol_header[18:19]
            self.writer.route_reply(RouteReply(source, destination, flag, time_to_live, previous_node, end_node, metric), neighbor_node)
        # if flag == b'5':
        #     unreachable_node = protocol_header[10:14]
        #     self.writer.route_error(RouteError(source, destination, flag, time_to_live, unreachable_node))
        if flag == b'6':
            # when node is unreachable via request 

    # Parsers the header of the incoming message.
    # @protocol_header    contains the protocol message header. 
    # @neighbor_node      previous node that forwarded the message.
    def parse_protocol_header(self, protocol_header, neighbor_node):                   
        source = protocol_header[:4]
        destination = protocol_header[4:8]
        flag = protocol_header[8:9]
        time_to_live = protocol_header[9:10]
        self.parse_header_flag(source, destination, flag, time_to_live, protocol_header, neighbor_node) 

    # Parses incoming byte stream. 
    # @mcu_header   mcu message part.
    # @protocol_header protocol message part.
    def parse_incoming_message(self, mcu_header, protocol_header):
        neighbor_node = mcu_header[3:7]
        if mcu_header[:2] == b'LR':
            self.parse_protocol_header(protocol_header, neighbor_node)
        else:
            pass


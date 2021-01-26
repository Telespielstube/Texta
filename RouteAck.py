from MessageHeader import MessageHeader

class RouteAck(MessageHeader):

    # defines a struct-like object for route acknowledgement message.
    def __init__(self, source, flag, time_to_live, origin_node, ack_node):
        super().__init__(source, flag, time_to_live)
        self.origin_node = origin_node
        self.ack_node = ack_node #node that sends the acknowledgement.
    
    # def __str__(self):
    #     return self.source + str(self.flag) + str(self.time_to_live) + self.ack_node
   
    

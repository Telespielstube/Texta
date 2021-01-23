from MessageHeader import MessageHeader

class RouteAck(MessageHeader):

    # defines a struct-like object for route acknowledgement message.
    def __init__(self, source, flag, time_to_live, ack_node):
        super().__init__(source, flag, time_to_live)
        self.ack_node = ack_node #neighbor node the textmessage was sent to.
    
    # def __str__(self):
    #     return self.source + str(self.flag) + str(self.time_to_live) + self.ack_node
   
    

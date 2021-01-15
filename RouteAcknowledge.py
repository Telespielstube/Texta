from MessageHeader import MessageHeader

class RouteAcknowledge(MessageHeader):

    def __init__(self, source, flag, time_to_live, ack_node):
        super().__init__(source, flag, time_to_live)
        self.ack_node = ack_node
    
    def __str__(self):
        return self.source + str(self.flag) + str(self.time_to_live) + self.ack_node
   
    

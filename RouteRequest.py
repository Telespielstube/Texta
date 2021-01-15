from MessageHeader import MessageHeader

class RouteRequest(MessageHeader):

    def __init__(self, source, flag, time_to_live, hop, requested_node):
        super().__init__(source, flag, time_to_live)
        self.hop = hop 
        self.requested_node = requested_node

    def __str__(self):
        return self.source.decode() + str(self.flag) + str(self.time_to_live) + str(self.hop) + self.requested_node.decode()
   
    # Adds 1 to the route cost by converting bytes to int and backwards
    def increment_hop(self):
        return self.hop + 1
       

from MessageHeader import MessageHeader

class RouteRequest(MessageHeader):

    def __init__(self, source, flag, time_to_live, hop, requested_node):
        super().__init__(source, flag, time_to_live)
        self.hop = hop 
        self.requested_node = requested_node

    # def __len__(self):
    #     return len(self.source) + len(str(self.flag)) + len(str(self.time_to_live)) + len(str(self.hop)) + len(self.requested_node)
    # def __str__(self):
    #     return self.source + str(self.flag) + str(self.time_to_live) + str(self.hop) + self.requested_node
   
    # Adds 1 to the route cost by converting bytes to int 
    def increment_hop(self):
        return int(self.hop.decode()) + 1
       

from MessageHeader import MessageHeader

class RouteReply(MessageHeader):

    def __init__(self, source, flag, time_to_live, hop, end_node, next_node):
        super().__init__(source, flag, time_to_live)
        self.hop = hop
        self.end_node = end_node # request message origin
        self.next_node = next_node # Neighbor who sent the request
        
    # Adds 1 to the route cost.
    def increment_hop(self):
        self.hop += 1
        



from MessageHeader import MessageHeader

class RouteRequest(MessageHeader):

    def __init__(self, source, flag, time_to_live, hop, requested_node):
        super().__init__(source, flag, time_to_live)
        self.hop = hop 
        self.requested_node = requested_node
   
    # Adds 1 to the route cost.
    def increment_hop(self):
        self.hop += 1
       

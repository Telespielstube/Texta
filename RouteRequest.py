from MessageHeader import MessageHeader

class RouteRequest(MessageHeader):

    def __init__(self, source, flag, time_to_live, hop, requested_node):
        super().__init__(source, flag, time_to_live)
        self.hop = hop 
        self.requested_node = requested_node

    def __str__(self):
        return (str(self.source, 'utf-8') + '\t' + str(self.flag, 'utf-8') + '\t' +str(self.time_to_live) + '\t' +str(self.hop) + '\t' +str(self.requested_node))
   
    # Adds 1 to the route cost by converting bytes to int and backwards
    def increment_hop(self, hop):
        return hop + 1
       
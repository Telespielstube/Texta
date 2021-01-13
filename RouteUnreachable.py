from MessageHeader import MessageHeader

class RouteUnreachable(MessageHeader):

    def __init__(self, source, flag, time_to_live, unreachable_node):
        super().__init__(source, flag, time_to_live)
        self.unreachable_node = unreachable_node
    
    def __str__(self):
        return self.source.decode('utf-8') + str(self.flag) + str(self.time_to_live) + self.unreachable_node.decode('utf-8')
   
    

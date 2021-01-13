from MessageHeader import MessageHeader

class RouteError(MessageHeader):

    def __init__(self, source, flag, time_to_live, broken_node):
        super().__init__(source, flag, time_to_live)
        self.broken_node = broken_node

    def __str__(self):
        return self.source.decode('utf-8') + str(self.flag) + str(self.time_to_live) + self.broken_node.decode('utf-8')
   
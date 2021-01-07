from MessageHeader import MessageHeader

class RouteError(MessageHeader):

    def __init__(self, source, destination, flag, time_to_live, broken_node):
        super().__init__(source, destination, flag, time_to_live)
        self.broken_node = broken_node
from MessageHeader import MessageHeader

class RouteError(MessageHeader):

    def __init__(self, source, destination, flag, time_to_live, unreachable_node):
        super().__init__(source, destination, flag, time_to_live)
        self.unreachable_node = unreachable_node
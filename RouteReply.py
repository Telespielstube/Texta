from MessageHeader import MessageHeader

class RouteReply(MessageHeader):

    def __init__(self, source, destination, flag, time_to_live, previous_node, end_node, metric):
        super().__init__(source, destination, flag, time_to_live)
        self.previous_node = previous_node
        self.end_node = end_node
        self.metric = metric



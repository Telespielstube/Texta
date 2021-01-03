from MessageHeader import MessageHeader

class RouteRequest(MessageHeader):

    def __init__(self, source, destination, flag, time_to_live, requested_node, metric):
        MessageHeader.__init__(self, source, destination, flag, time_to_live)
        self.requested_node = requested_node
        self.metric = metric # route cost to the node

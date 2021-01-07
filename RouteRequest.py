from MessageHeader import MessageHeader

class RouteRequest(MessageHeader):

    def __init__(self, source, flag, time_to_live, requested_node, metric):
        super().__init__(source, flag, time_to_live)
        self.requested_node = requested_node
        self.metric = metric # route cost to the node

    # Adds 1 to the route cost
    def increment_metric(self, metric):
        return self.metric + 1


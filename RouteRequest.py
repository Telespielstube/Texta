from MessageHeader import MessageHeader

class RouteRequest(MessageHeader):

    def __init__(self, source, destination, flag, time_to_live, requested_node, metric):
        MessageHeader.__init__(self, source, destination, flag, time_to_live)
        self.requested_node = requested_node
        self.metric = metric # route cost to the node

    # Decrement time to live value
    def decrement_time_to_live(self, time_to_live):
        return time_to_live - 1
        
    # Adds 1 to the route cost
    def increment_metric(self, metric):
        return metric + 1

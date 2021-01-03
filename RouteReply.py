from MessageHeader import MessageHeader

class RouteReply(MessageHeader):

    def __init__(self, source, destination, flag, time_to_live, previous_node, end_node, metric):
        MessageHeader.__init__(self, source, destination, flag, time_to_live)
        self.previous_node = previous_node
        self.end_node = end_node
        self.metric = metric

    # Adds 1 to the route cost
    def increment_metric(self):
        return self.metric + 1

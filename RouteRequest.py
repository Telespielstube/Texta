from MessageHeader import MessageHeader

class RouteRequest(MessageHeader):

    def __init__(self, source, destination, flag, time_to_live, requested_node, metric):
        MessageHeader.__init__(self, source, destination, flag, time_to_live)
        self.requested_node = requested_node
        self.metric = metric # route cost to the node

    @property
    def requested_node(self):
        return self.__requested_node
    
    @requested_node.setter  
    def requested_node(self, requested_node):
        self.__requested_node = requested_node

    @property
    def metric(self):
        return self.__metric

    @metric.setter
    def metric(self, metric):
        self.__metric = metric

    # Adds 1 to the route cost
    def increment_metric(self):
        return self.metric + 1

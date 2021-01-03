from MessageHeader import MessageHeader

class RouteReply(MessageHeader):

    def __init__(self, source, destination, flag, time_to_live, previous_node, end_node, metric):
        MessageHeader.__init__(self, source, destination, flag, time_to_live)
        self.previous_node = previous_node
        self.end_node = end_node
        self.metric = metric

    @property
    def previous_node(self):
        return self.__previous_node
    
    @previous_node.setter  
    def previous_node(self, previous_node):
        self.__previous_node = previous_node

    @property
    def end_node(self):
        return self.__end_node
    
    @end_node.setter  
    def end_node(self, end_node):
        self.__end_node = end_node

    @property
    def metic(self):
        return self.__metic

    @metic.setter
    def metic(self, metic):
        self.__metic = metic

    # Adds 1 to the route cost
    def increment_metric(self):
        return self.metric + 1

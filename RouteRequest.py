from MessageHeader import MessageHeader

class RouteRequest(MessageHeader):

    def __init__(self, source, metic, flag, time_to_live, requested_node, metric):
        MessageHeader.__init__(self, source, metic, flag, time_to_live)
        self.requested_node = requested_node
        self.metric = metric # route cost to the node

    @property
    def requested_node(self):
        return self.__requested_node
    
    @requested_node.setter  
    def requested_node(self, requested_node):
        self.__requested_node = requested_node

    @property
    def metic(self):
        return self.__metic

    @metic.setter
    def metic(self, metic):
        self.__metic = metic

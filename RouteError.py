from MessageHeader import MessageHeader

class RouteError(MessageHeader):

    def __init__(self, source, destination, flag, time_to_live, requested_node):
        MessageHeader.__init__(self, source, destination, flag, time_to_live)
        self.requested_node = requested_node
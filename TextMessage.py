from MessageHeader import MessageHeader

class TextMessage(MessageHeader):

    def __init__(self, source, destination, flag, time_to_live, next_node, payload):
        super().__init__(source, destination, flag, time_to_live)
        self.next_node = next_node
        self.payload = payload 
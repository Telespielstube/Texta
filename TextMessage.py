from MessageHeader import MessageHeader

class TextMessage(MessageHeader):

    def __init__(self, source, flag, time_to_live, destination, next_node, payload):
        super().__init__(source, flag, time_to_live)
        self.destination = destination
        self.next_node = next_node
        self.payload = payload 

    # Represents the object as utf-8 string.    
    def __str__(self):
        return (self.source.decode('utf-8') + str(self.flag) + str(self.time_to_live) + str(self.destination) + str(self.next_node) + str(self.payload))

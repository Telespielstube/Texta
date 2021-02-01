import hashlib

from MessageHeader import MessageHeader

class TextMessage(MessageHeader):

    def __init__(self, source, flag, time_to_live, destination, next_node, payload):
        super().__init__(source, flag, time_to_live)
        self.destination = destination
        self.next_node = next_node
        self.payload = payload 

    def create_hash(self):    
        hashed = hashlib.md5(self.source + self.payload)
        hex_hash = hashed.hexdigest()
        return hex_hash[:6]

    # # Represents the object as utf-8 string.    
    # def __str__(self):
    #     return self.source + str(self.flag) + str(self.time_to_live) + str(self.destination) + self.next_node + str(self.payload)
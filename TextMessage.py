import hashlib

from MessageHeader import MessageHeader

class TextMessage(MessageHeader):

    def __init__(self, source, flag, time_to_live, destination, next_node, payload):
        super().__init__(source, flag, time_to_live)
        self.destination = destination
        self.next_node = next_node
        self.payload = payload 

    def create_hash(self, MY_ADDRESS):    
        hashed = hashlib.md5(MY_ADDRESS + self.payload)
        hex_hash = hashed.hexdigest()
        return hex_hash[:6]
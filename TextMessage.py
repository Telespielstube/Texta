import hashlib

from MessageHeader import MessageHeader

class TextMessage(MessageHeader):

    def __init__(self, source, flag, time_to_live, destination, next_node, payload):
        super().__init__(source, flag, time_to_live)
        self.destination = destination
        self.next_node = next_node
        self.payload = payload 

    def create_hash(self, source, payload):   
        self.payload.decode('utf-8') 
        hashed = hashlib.md5(source + payload).hexdigest()
        print('Hash for ack message: ' + hashed)
        return hashed[:6]
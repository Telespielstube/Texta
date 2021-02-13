import hashlib
class UserMessage:
    
    def __init__(self, message, destination):
        self.message = message
        self.destination = destination

    def create_hash(self, MY_ADDRESS):    
        hashed = hashlib.md5(MY_ADDRESS + self.message.encode())
        hex_hash = hashed.hexdigest()
        return hex_hash[:6]
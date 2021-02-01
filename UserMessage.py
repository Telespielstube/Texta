import hashlib
class UserMessage:
    
    def __init__(self, command, message, destination):
        self.command = command
        self.message = message
        self.destination = destination

    def create_hash(self, MY_ADDRESS):    
        hashed = hashlib.md5(MY_ADDRESS + self.message.encode())
        hex_hash = hashed.hexdigest()
        return hex_hash[:6]

    # def __str__(self):
    #     return str(self.command) + str(self.message) + str(self.destination)
class MessageItem:
    
    def __init__(self, command, message, destination=None):
        self.command = command
        self.message = message
        self.destination = destination

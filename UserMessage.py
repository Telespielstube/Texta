class UserMessage:
    
    def __init__(self, command, message, destination):
        self.command = command
        self.message = message
        self.destination = destination

    def __str__(self):
        return self.command + self.message + self.destination
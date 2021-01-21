class UserMessage:
    
    def __init__(self, command, message, destination):
        self.command = command
        self.message = message
        self.destination = destination

    # def __str__(self):
    #     return str(self.command) + str(self.message) + str(self.destination)
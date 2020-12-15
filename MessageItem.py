class MessageItem():
    
    # Constructor for Message Object.
    # @command   
    # @write_lock   locks the writing process to the mcu
    def __init__(self, command, message, destination=None):
        self.command = command
        self.message = message
        self.destination = destination

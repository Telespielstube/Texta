class UserMessage:
    
    def __init__(self, command=None, message=None, destination=None):
        self.command = command
        self.message = message
        self.destination = destination

    def __str__(self):
        return self.command + self.message + self.destination

    # Finds the matching table entry for the waiting message
    def get_pending_message_route(self, routing_table, pending_message_list):
        for message in pending_message_list:
            for route in routing_table:
                if message.destination is route.destination:
                    found_message = message
                return found_message 
 
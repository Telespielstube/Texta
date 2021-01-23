from RoutingTable import RoutingTable 
class PendingMessage:

    # defines a c-style struct for pending messages.
    def __init__(self, message, retry):
        self.message = message
        self.retry = retry

       
    
 
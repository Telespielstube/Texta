from RoutingTable import RoutingTable 
class PendingMessage:

    # defines a struct like object for pending messages.
    def __init__(self, message, retry):
        self.message = message
        self.retry = retry

       
    
 
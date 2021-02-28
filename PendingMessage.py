from RoutingTable import RoutingTable 
class PendingMessage:

    # defines a struct like object for pending messages.
    # @message      holds the UserMessage object.
    # @retry        attempts to send UserMessage.
    def __init__(self, message, timestamp, retry):
        self.message = message
        self.timestamp = timestamp
        self.retry = retry

       
    
 
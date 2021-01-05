class MessageHeader:

    def __init__(self, source, destination, flag, time_to_live):
        self.source = source
        self.destination = destination
        self.flag = flag
        self.time_to_live = time_to_live

    # Decrement time to live value
    def decrement_time_to_live(self, time_to_live):
        return time_to_live - 1
        
    # Adds 1 to the route cost
    def increment_metric(self, metric):
        return self.metric + 1






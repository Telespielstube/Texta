class MessageHeader:

    def __init__(self, source=None, flag=int, time_to_live=int):
        self.source = source
        self.flag = flag
        self.time_to_live = time_to_live

    # Decrement time to live value
    def decrement_time_to_live(self):
        decremented_ttl = self.time_to_live - 1
        return decremented_ttl







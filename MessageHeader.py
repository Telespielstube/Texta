class MessageHeader:

    def __init__(self, source, flag, time_to_live):
        self.source = source
        self.flag = flag
        self.time_to_live = time_to_live

    # Decrement time to live value
    def decrement_time_to_live(self):
        return int(self.time_to_live) - 1
        







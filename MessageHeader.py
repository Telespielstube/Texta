class MessageHeader:

    def __init__(self, source, destination, flag, time_to_live):
        self.source = source
        self.destination = destination
        self.flag = flag
        self.ttl = time_to_live
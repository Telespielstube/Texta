class MessageHeader:

    def __init__(self, source, destination, flag, time_to_live):
        self.source = source
        self.destination = destination
        self.flag = flag
        self.ttl = time_to_live

    @property
    def source(self):
        return self.__source
    
    @source.setter  
    def source(self, source):
        self.__source = source

    @property
    def destination(self):
        return self.__destination

    @destination.setter
    def destination(self, destination):
        self.__destination = destination

    @property
    def flag(self):
        return self.__flag
    
    @flag.setter
    def flag(self, flag):
        self.__flag = flag

    @property
    def time_to_live(self):
        return self.__time_to_live
    
    @time_to_live.setter
    def time_to_live(self, time_to_live):
        self.__time_to_live = time_to_live

    # Subracts 1 from time to live header field.
    def decrement_ttl(self):
        decremented_ttl = self.time_to_live - 1
        return decremented_ttl
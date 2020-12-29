class Header():

    def __init__(self):
        self.source = b''
        self.destination = b''
        self.flag = 0
        self.time_to_live = 0 
    
    # @property
    # def source(self):
    #     return self.__source
    
    # @source.setter
    # def source(self, source):
    #     self.__source = source 

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

    # Calculates the time to live for packets.
    def calc_ttl(self):
        decremented_ttl = self.time_to_live - 1
        return decremented_ttl

    # def build_route_request_message(self):
    #     return 

    # def build_route_reply_message(self):
    #     return

    # def build_route_request_header(self):
    
    # def build_route_reply_header(self):

    # # Build the message header
    # def build_header(self, source):
    #     if self.flag == 3:
    #         msg_header = source + destination + str(self.flag) + str(self.time_to_live)
    #     return (source + self.destination + str(self.flag) + str(self.time_to_live)) 

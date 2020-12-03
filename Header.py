class Header():

    def __init__(self):
        self.destination = ''
        self.source = ''
        self.flag = 0
        # self.time_to_live = 0 #probably start at 20
        # self.sequence_num = 0
        # self.seq_num_table = dict()
    
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

    @property
    def address(self):
        return self.__MY_ADDRESS
    
    @address.setter
    def address(self, MY_ADDRESS):
        self.__MY_ADDRESS = MY_ADDRESS

    # # Calculates the time to live for packets.
    # def calc_ttl(self):
    #     decremented_ttl = self.time_to_live - 1
    #     return decremented_ttl
    
    # @property
    # def sequence_num(self):
    #     return self.__sequence_num
    
    # @sequence_num.setter
    # def sequence_num(self, sequence_num):
    #     self.__sequence_num = sequence_num

    # def add_sequence_number(self, seq_num):
    #     if (self.sequence_num < seq_num):
    #         self.seq_num_table[self.source] = seq_num

    # # Build the message header
    # def build_header(self, destination, MY_ADDRESS):
    #      return str(self.flag).zfill(2) + destination + MY_ADDRESS + str(self.time_to_live).zfill(2) + str(self.sequence_num).zfill(2)

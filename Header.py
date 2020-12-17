class Header():

    def __init__(self):
        self.source = b''
        self.destination = b''
        self.flag = 0
        # self.time_to_live = 0 #probably start at 8
    
    @property
    def source(self):
        return self.__source
    
    @address.setter
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

    #
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

    # Build the message header
    def build_header(self, source, destination):
         return (self.source + self.destination + self.flag) #+ self.time_to_live() + self.sequence_num()))

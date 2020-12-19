from datetime import datetime

class Node(object):

    def __init__(self, address):
        self.address = address #address of the node
        #self.hop = hop #neighbor node


    def __del__(self):
        print ("Object delete")

    def __repr__(self):
        return (self. address)

    def __str__(self):
        return self.address 
    
    __repr__ = __str__
    
    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        self.__address = address 

    # @property
    # def hop(self):
    #     return self.__hop
    
    # @hop.setter
    # def hop(self, hop):
    #     self.__hop = hop
    
    # @property
    # def time_stamp(self):
    #     return self.__time_stamp
    
    # @time_stamp.setter
    # def time_stamp(self, time_stamp):
    #     self.__time_stamp = time_stamp
        
    # # Regularyly updates timestamp of the calling node.
    # def update_time_stamp(self):     
    #     now = datetime.now()   
    #     self.time_stamp = datetime.timestamp(now)

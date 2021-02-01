import hashlib

from MessageHeader import MessageHeader

class RouteAck(MessageHeader):

    # defines a struct-like object for route acknowledgement message.
    def __init__(self, source, flag, time_to_live, hash_value):
        super().__init__(source, flag, time_to_live)
        self.hash_value = hash_value #md5 generated value by concatenate source address and payload 
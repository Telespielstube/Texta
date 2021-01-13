from MessageHeader import MessageHeader

class TextMessage(MessageHeader):

    def __init__(self, source, flag, time_to_live, destination, next_node, payload):
        super().__init__(source, flag, time_to_live)
        self.destination = destination
        self.next_node = next_node
        self.payload = payload 

    # Represents the object as utf-8 string.    
    def __str__(self):
<<<<<<< HEAD
<<<<<<< HEAD
        return self.source.decode() + str(self.flag) + str(self.time_to_live) + self.destination.decode() + self.next_node.decode() + str(self.payload)
=======
        return self.source.decode() + str(self.flag) + str(self.time_to_live) + str(self.destination) + self.next_node.decode() + str(self.payload)
>>>>>>> 83aadf243d8b027e20bdd7c71263458f6f8e714a
=======
        return self.source.decode() + str(self.flag) + str(self.time_to_live) + str(self.destination) + self.next_node.decode() + str(self.payload)
>>>>>>> 83aadf243d8b027e20bdd7c71263458f6f8e714a

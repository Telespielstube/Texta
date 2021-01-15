class Route:

    def __init__(self, destination, neighbor, hop):
        self.destination = destination
        self.neighbor = neighbor
        self.hop = hop
    
    def __str__(self):
        return self.destination + '\t' + self.neighbor + '\t' + str(self.hop)

    

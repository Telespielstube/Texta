class Route:

    def __init__(self, destination, neighbor, hop):
        self.destination = destination
        self.neighbor = neighbor
        self.hop = hop
    
    def __str__(self):
        return (str(self.destination, 'utf-8') + '\t' + str(self.neighbor, 'utf-8') + '\t' + str(self.hop))

    
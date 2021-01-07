class Route:

    def __init__(self, destination=None, neighbor=None, hop=None):
        self.neighbor = neighbor
        self.destination = destination
        self.hop = hop
    
    def __str__(self):
        return self

    
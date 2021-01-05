class Route:

    def __init__(self, neighbor=None, destination=None, metric=None):
        self.neighbor = neighbor
        self.destination = destination
        self.metric = metric

    # def __repr__(self):
    #     return {self. address, self.hop, self.metric}

    # def __str__(self):
    #     return self.address + ', ' + str(self.hop) + ', ' + str(self.metric)
    
    # __repr__ = __str__
    
    # def __str__(self):
    #     return self

    
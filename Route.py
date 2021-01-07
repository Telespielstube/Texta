class Route:

    def __init__(self, neighbor=None, destination=None, metric=None):
        self.neighbor = neighbor
        self.destination = destination
        self.metric = metric
    
    def __str__(self):
        return self

    
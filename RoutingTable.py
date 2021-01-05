from Route import Route
class RoutingTable():
    
    # Constructor
    # @routing_table   inizialises a list. A list allows duplicates.
    def __init__(self):
        self.routing_table = [] 
        self.route = Route(b'', b'', 0)

    # Adds a new address to the routing table.
    # @neighbor
    def add_route_to_table(self, neighbor, destination, metric): # hop, metric):
        routing_table.append(self.route(neighbor, destination, metric)) 
        print('Route added')

    # Prints all Nodes in routing table as readable string.   
    def show_routing_table(self):
        for entry in self.routing_table:
            print (str(entry.neighbor) + ' ' + str(entry.destination) + ' ' + str(entry.metric))

    # Finds the route with the lowest costs to the destination node.
    # @destination    destination node to be found in list
    # @return         neighbor node through which the destination can be reached the fastest 
    def find_best_route(self, destination):
        sorted_list = sorted(self.routing_table, key=lambda x: x.metric)
        for entry in sorted_list:
            if entry.destination is destination:
                neighbor = destination
        return neighbor 


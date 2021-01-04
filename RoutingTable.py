from Route import Route
class RoutingTable():
    
    # Constructor
    # @routing_table   inizialises a list. A list allows duplicates.
    def __init__(self):
        self.routing_table = [] 
        self.route = Route(b'', b'', 0)

    # Adds a new address to the routing table.
    # @address = address to add to table
    def add_route_to_table(self, neighbor, destination, metric): # hop, metric):
        routing_table.append(self.route(neighbor, destination, metric)) 
        print('Route added')

    # Prints all Nodes in routing table.   
    def show_routing_table(self):
        for entry in self.routing_table:
            print (entry.neighbor + ' ' + entry.destination + ' ' + entry.metric)

    def find_best_route(self, destination):
        sorted_list = sorted(self.routing_table, key=self.route.metric)
        for entry in sorted_list:
            neighbor = entry.neighbor
            
        return neighbor, 


from Route import Route
class RoutingTable():
    
    # Constructor
    # @routing_table   inizialises a list. A list allows duplicates.
    def __init__(self, MY_ADDRESS, metric):
        self.routing_table = [] 
        self.add_route_to_table.append(Route(MY_ADDRESS, MY_ADDRESS, 0)

    # Adds a new address to the routing table.
    # @neighbor
    def add_route_to_table(self, neighbor, destination, metric): 
        self.routing_table.append(Route(destination, neighbor, metric)) 
        print('Route added')

    # Prints all Nodes in routing table as readable string.   
    def show_routing_table(self):
        for entry in self.routing_table:
            print (Route)
    
    # Find entry in unsorted routing table
    # @node     node to be found in routing table
    # @return   found node  
    def find_entry(self, node):
        found = b''
        for entry in self.routing_table:
            if entry.source is node:
                found = entry.source
        return found

    # Finds the route with the lowest costs to the destination node.
    # @destination    destination node to be found in list
    # @return         neighbor node through which the destination can be reached the fastest 
    def find_best_route(self, destination):
        byte_dest = b'destination'
        sorted_list = sorted(self.routing_table, key=lambda x: x.metric)
        neighbor = b''
        for entry in sorted_list:
            if entry.destination is byte_dest:
                neighbor = entry.destination
        return neighbor 


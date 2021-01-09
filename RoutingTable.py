from Route import Route
class RoutingTable():
    
    # Constructor
    # @routing_table   inizialises a list. A list allows duplicates.
    def __init__(self, MY_ADDRESS, metric):
        self.routing_table = [] 
        self.add_route_to_table(MY_ADDRESS, MY_ADDRESS, 0)

    # Adds a new address to the routing table.
    # @destination Destination node
    # @neighbor    neighbor node
    # @hop         Route cost to destination
    def add_route_to_table(self, destination, neighbor, hop): 
        self.routing_table.append(Route(destination, neighbor, hop)) 
        print('Route added')

    # Removes a given entry from the list
    # @node    the node to be removed
    def remove_route_from_table(self, node):
        self.routing_table.remove(node)

    # Prints all Nodes in routing table as readable string.   
    def show_routing_table(self):
        for entry in self.routing_table:
            print (entry)
    
    # Find entry in unsorted routing table
    # @node     node to be found in routing table
    # @return   found node  
    def find_entry(self, node):
        found = b''
        for entry in self.routing_table:
            if entry.destination is node:
                found = entry.source
        return found

    # Finds the route with the lowest costs to the destination node.
    # @destination    destination node to be found in list
    # @return         neighbor node through which the destination can be reached the fastest 
    def find_best_route(self, destination):
        sorted_list = sorted(self.routing_table, key=lambda x: x.hop)
        neighbor = b''
        for entry in sorted_list:
            if entry.destination == destination:
                neighbor = entry.destination
                print(neighbor)
        return neighbor 


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
    def remove_route_from_table(self, broken_node):
        for entry in self.routing_table:
            if entry.destination is broken_node or entry.neighbor is broken_node:
                self.routing_table.remove(entry.destination, entry.neighbor, entry.hop)

    # Prints all Nodes in routing table as readable string.   
    def show_routing_table(self):
        for entry in self.routing_table:
            print ('|\s\s\s' + entry.source + '\s\s\s|' + '\s\s\s' + entry.neighbor + '\s\s\s|' + '\s\s\s' + entry.hop + '\s\s\s|' )
    
    # Find entry in unsorted routing table
    # @node     node address to be found in routing table
    # @return   found node address  
    def search_entry(self, node):
        found = False
        for entry in self.routing_table:
            if entry.destination == node:
                found = True
        return found

    # Finds the route with the lowest costs to the destination node by sorting the table by the hop field.
    # @node           node node to be found in table 
    # @return         neighbor node the destination can be reached the fastest 
    def find_route(self, node):
        neighbor = b''
        for entry in sorted(self.routing_table, key=lambda Route: Route.hop):
            if entry.destination == node.encode():
               neighbor = entry.neighbor
        return neighbor


from Route import Route
class RoutingTable():
    
    # Constructor
    # @routing_table   inizialises a list. A list allows duplicates.
    def __init__(self, MY_ADDRESS, metric):
        self.table = dict() 
        self.add_route_to_table(MY_ADDRESS, MY_ADDRESS, 0)

    # Adds a new address to the routing table.
    # @destination Destination node
    # @neighbor    neighbor node
    # @hop         Route cost to destination
    def add_route_to_table(self, destination, neighbor, hop): 
        self.table[destination] = Route(destination, neighbor, hop)
        print('Route added')
        
    # Removes a given entry from the list
    # @node    the node to be removed
    def remove_route_from_table(self, broken_node):
        for key, value in list(self.table.items()):
            if value.destination == broken_node or value.neighbor == broken_node:
                del [key]  

    # Prints all Nodes in routing table as readable string.   
    def show_routing_table(self):
        for key, value in self.table.items():
            print ('|  ' + key.decode() + '  |' + '   ' + value.neighbor.decode() + '   |' + '  ' + str(value.hop) + '  |' )
        print('---------------------------')
    # Find entry in unsorted routing table
    # @node     node address to be found in routing table
    # @return   found node address  
    def search_entry(self, node):
        found = False
        for key in self.table.keys():
            if key == node:
                found = True
        return found

    # Finds the route with the lowest costs to the destination node by sorting the table by the hop field.
    # @node           destination node to be found in table 
    # @return         neighbor node the destination can be reached the fastest 
    def find_route(self, node):
        neighbor = b''
        for key, value in self.table.items():
            if key == node.encode():
                neighbor = value.neighbor
        return neighbor
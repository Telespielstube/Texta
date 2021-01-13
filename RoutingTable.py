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

    # Finds duplicated routes 
    def find_route_in_table(self, request, neighbor):
        found = True
        for entry in self.routing_table:
            if entry.destination is request.source and entry.neighbor == neighbor and entry.hop is request.hop:
                found = True
            else:
                found = False
            return found

    # Removes a given entry from the list
    # @node    the node to be removed
    def remove_route_from_table(self, broken_node):
        self.routing_table.remove(broken_node)

    # Prints all Nodes in routing table as readable string.   
    def show_routing_table(self):
        for entry in self.routing_table:
            print (entry)
    
    # Find entry in unsorted routing table
    # @node     node address to be found in routing table
    # @return   found node address  
    def find_entry(self, node):
        found = b''
        for entry in self.routing_table:
            if entry.destination is node:
                found = entry.source
        return found

    # Finds the route with the lowest costs to the destination node by sorting the table by the hop field.
    # @destination    destination node to be found in 
    # @return         neighbor node through which the destination can be reached the fastest 
    def find_best_route(self, destination):
        sorted_list = sorted(self.routing_table, key=lambda x: x.hop)
        for entry in sorted_list:
            if entry.destination == destination:
               neighbor = entry.neighbor 
        return neighbor 


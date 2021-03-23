import threading
from Route import Route
class RoutingTable():
    
    # Constructor
    # @routing_table   inizialises a list. A list allows duplicates.
    def __init__(self, MY_ADDRESS, metric):
        self.table = dict()
        self.table_lock = threading.Lock() 
        self.add_route_to_table(MY_ADDRESS, MY_ADDRESS, 0)
        
    # # Locks a code block for safely read from and write to a resource. 
    def lock(self):
        self.table_lock.acquire()

    # # releases a locked code block. 
    def unlock(self):
        self.table_lock.release()

    # Adds a new address to the routing table.
    # @destination Destination node
    # @neighbor    neighbor node
    # @hop         Route cost to destination
    def add_route_to_table(self, destination, neighbor, hop): 
        self.lock()
        self.table[destination] = Route(destination, neighbor, hop)
        self.unlock()
        print(destination.decode() + ' added')
        
    # Removes a given entry from the list
    # @node    the node to be removed
    def remove_route_from_table(self, broken_node):
        self.lock()
        deleted_node = None
        for key, value in list(self.table.items()):
            if value.destination == broken_node or value.neighbor == broken_node: 
                deleted_node = self.table.pop(key, None) 
        self.unlock()
        return deleted_node

    # Prints all Nodes in routing table as readable string.   
    def show_routing_table(self):
        for key, value in self.table.items():
            print ('|  ' + key.decode() + '  |' + '   ' + value.neighbor.decode() + '   |' + '  ' + str(value.hop) + '  |' )
        print('---------------------------')
    
    # Searches entry in routing table
    # @node     node address to be found in routing table
    # @return   found node address  
    def search_entry(self, node):
        found = False
        for key, value in self.table.items():
            if key == node or value.neighbor == node:
                found = True
        return found

    # Finds the route to the destination node by finding the neighbor connected to the destination.
    # @node           destination node to be found in table 
    # @return         neighbor node the destination can be reached the fastest 
    def find_route(self, node):
        for key, value in self.table.items():
            if key == node or value == node: 
                return self.table.get(key)        

        
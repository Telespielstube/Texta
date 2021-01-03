from Route import Route
class RoutingTable():
    
    # Constructor
    # @routing_table   inizialises a dictionary (is a collection which is unordered, changeable and does not allow duplicates.)
    def __init__(self):
        self.routing_table = dict()
        self.route = Route(b'0', 0)

    # Adds a new address to the routing table.
    # @address = address to add to table
    def add_address_to_table(self, address): # hop, metric):
        if address not in self.routing_table:
           # self.routing_table[address] = Node(address)  
            print('Node added' + address.decode())

    # Prints all Nodes in routing table.   
    def show_routing_table(self):
        for key in self.routing_table.items():
            print (key.decode())

    # Finds an address in the routing table.
    # @address = address to look for in table
    # @exception = if address in not found  
    def find_entry(self, address):
        entry = b''
        try:
            entry = self.routing_table.get(address)
        except KeyError:
            entry = b'0'
        return entry

    #def find_best_route(self):
        


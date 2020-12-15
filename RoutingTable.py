from Node import Node
from datetime import datetime
import collections

class RoutingTable():
    
    # Constructor
    # @routing_table   inizialises a dictionary (is a collection which is unordered, changeable and does not allow duplicates.)
    def __init__(self):
        self.routing_table = dict()

    # Adds a new address to the routing table.
    # @address = address to add to table
    def add_address_to_table(self, address): # hop, metric):
        if address not in self.routing_table:
            self.routing_table[address] = Node(address)   #, hop, metric)
            print('Node added' + address)
        else:
            print(address)

    # Prints all Nodes in routing table.   
    def show_routing_table(self):
        for key in self.routing_table.items():
            print (key)

      
          
          
            # node = self.find_entry(address)
            # node.update_time_stamp()
            # self.routing_table[address] = node

    # # Finds an address in the routing table.
    # # @address = address to look for in table
    # # @exception = if address in not found  
    # def find_entry(self, address):
    #     try:
    #         return self.routing_table.get(address)
    #     except KeyError:
    #         print("Address not found.")

    # # Regularyly checks the table if Node is still active
    # def remove_vacant_nodes(self, loop):
    #     while True:
    #         #await asyncio.sleep(30)
    #         print("Removing vancant nodes.")
    #         #current time and date
    #         now = datetime.now()
    #         current_time = datetime.timestamp(now)
    #         remove_nodes = []
    #         for node in self.routing_table.values():
    #             if current_time - node.time_stamp > 60.0: # if node has not send any message withing 60 sec. it gets deleted
    #                 remove_nodes.append(node.address)
    #         for address in remove_nodes:
    #             deleted_node = self.routing_table.pop(address, None)
    #             print("Inactive node deleted:", deleted_node.address)

    # # Sends routing table back to sender of a just received Hello packet
    # def build_routing_table(self):
    #     for value in self.routing_table.values():
    #         routing_table += value.address + value.hop 
    #     return routing_table
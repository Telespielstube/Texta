from RoutingTable import RoutingTable
from Header import Header
#from Node import Node

class Parser():

    def __init__(self, routing_table):
        self.routing_table = routing_table
        self.header = Header()
        #self.node = Node(0, 0, 0)
        
     # Parsers the header of the incoming message.
    # @header_string    contains the header + payload as string. 
    def parse_protocol_header(self, own_header):       
        self.header.source = own_header[:4]#set the sliced source adress as source adress in header class
        self.header.destination = own_header[4:8]
       # self.header.flag = own_header[8:9] # self.header.flag this is a setter call in Python    
       # self.header.time_to_live = own_header[9:10]

       # if self.header.flag == b'0':
        self.routing_table.add_address_to_table(self.header.source)

    # Parses incoming byte stream. 
    # @line         the incoming message received by the LoRa mcu.
    # @transport    serial communication channel to the mcu.
    def parse_incoming_message(self, mcu_header, protocol_header):
        splitted = mcu_header.decode().split(',')
        if splitted[0] == 'AT' and splitted[1] == 'OK' or splitted[0] == 'ERR: PARA' or splitted[0] == 'ERR: CMD' or splitted[0] == 'CPU: BUSY':
            pass
        if splitted[0] == 'LR':
            self.parse_protocol_header(protocol_header)
            

  
        # if self.header.flag == '00' and self.header.destination != self.connection.MY_ADDRESS:
        #     if self.header.calc_ttl() > 0:
        #         payload = len(header_string) - Parser.HEADER_LENGTH
        #         self.connection.foward_message(self.header.time_to_live, payload)
        #     else:
        #         pass
        # if self.header.flag == '00' and self.header.destination == self.connection.MY_ADDRESS:
        #     self.header.sequence_num += 1
        #     # no response for 3 retries remove node
        # if self.header.flag == '01':
        #     self.routing_table.add_address_to_table(self.header.source, 1, 1)
        #     #self.connection.transmit_queue.put(self.routing_table.send_routing_table())
        # if self.header.flag == '02':
        #     self.parse_payload(header_string[12:])
            # no response for 3 retries remove node
        # if self.header.flag == '05':
        #     self.node = self.routing_table.find_entry(self.header.destination)
        #     self.node.update_time_stamp()
        # else:
        #     pass
    
    # # Parses the payload to update the routing table.
    # # payload_string = contains received nodes and hops as string
    # def parse_payload(self, payload_string):
    #     sliced_payload = []
    #     hop = 2
    #     metric = 2
    #     n = 6
    #     for index in range(0, len(payload_string), n):
    #         sliced_payload.append(payload_string[index : index + n])
    #     for index in range(0, len(sliced_payload), 1):
    #         node_address = str(sliced_payload[index][:4])
    #         node_hop = sliced_payload[index][4:6]
    #         self.routing_table.add_address_to_table(node_address, node_hop, metric)
    #     hop +=1
    #     metric +=1

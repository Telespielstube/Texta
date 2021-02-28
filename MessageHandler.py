import threading, hashlib

from RoutingTable import RoutingTable
from PendingMessage import PendingMessage
from RouteRequest import RouteRequest
from RouteReply import RouteReply
from RouteError import RouteError
from RouteAck import RouteAck
from TextMessage import TextMessage
from UserMessage import UserMessage
from UserInterface import UserInterface
from PendingMessageTimer import PendingMessageTimer

class MessageHandler:

    def __init__(self, MY_ADDRESS, routing_table, writer):
        self.MY_ADDRESS = MY_ADDRESS
        self.routing_table = routing_table
        self.writer = writer
        self.pending_message_list = []
        self.ack_message_list = dict()
        self.list_lock = threading.Lock()

    def count_time():
        
    # Message from user interface
    # @user_message    user message object.      
    def user_input(self, user_message):
        route = self.routing_table.find_route(user_message.destination)
        if not route:  
            self.writer.send_message(self.writer.add_separator(RouteRequest(self.MY_ADDRESS, 3, 5, 0, user_message.destination))) 
            self.pending_message_list.append(PendingMessage(user_message, 0, 1)) 
        else:
            self.writer.send_message(self.writer.add_separator(TextMessage(self.MY_ADDRESS, 1, 5, user_message.destination, route, user_message.message)))
            self.ack_message_list[self.create_hash(self.MY_ADDRESS, user_message.message)] = (PendingMessage(TextMessage(self.MY_ADDRESS, 1, 5, user_message.destination, route, user_message.message), 0, 1))

    # Sends a request to all reachable nodes to find the requested node .
    # @request          Request message object.
    # @neighbor_node    Neighbor node address.       
    def route_request(self, request, neighbor_node):
        if request.source == self.MY_ADDRESS:
            del request
        elif request.requested_node == self.MY_ADDRESS: 
            if not self.routing_table.search_entry(request.source): 
                request.increment_hop()
                self.routing_table.add_route_to_table(request.source, neighbor_node, request.hop)     
            self.writer.send_message(self.writer.add_separator(RouteReply(self.MY_ADDRESS, 4, 5, 0, request.source, neighbor_node)))
        else:
            if not self.routing_table.search_entry(request.source): 
                request.increment_hop()
                self.routing_table.add_route_to_table(request.source, neighbor_node, request.hop)
            elif self.routing_table.search_entry(request.requested_node):  
                self.writer.send_message(self.writer.add_separator(RouteReply(request.source, 4, 5, 0, request.source, neighbor_node)))
            elif request.decrement_time_to_live() > 0:  
                request.increment_hop()
                self.writer.send_message(self.writer.add_separator(request))
                print('Request forwarded')
            else:
                del request
                
    # Sends a reply to the source node if own address matches request_messageed node.
    # RouteReply(source, destination, flag, time_to_live, previous_node, end_node, metric))
    # reply            Reply message object.
    # neighbor_node    Neighbor node address.
    def route_reply(self, reply, neighbor_node):
        if reply.source == self.MY_ADDRESS or reply.next_node != self.MY_ADDRESS:
            del reply   
        elif reply.next_node == self.MY_ADDRESS and reply.end_node == self.MY_ADDRESS: 
            reply.increment_hop()
            self.routing_table.add_route_to_table(reply.source, neighbor_node, reply.hop)
            self.process_pending_user_message()             
        elif reply.next_node == self.MY_ADDRESS and not self.routing_table.search_entry(reply.source) and reply.end_node != self.MY_ADDRESS:
            reply.increment_hop() 
            self.routing_table.add_route_to_table(reply.end_node, neighbor_node, reply.hop)
            if reply.decrement_time_to_live() > 0:                 
                self.writer.send_message(self.writer.add_separator(reply))
                print('Reply forwarded.')
            else: 
                del reply
           
    # Prepares the route message for sending. 
    # error    RouteError message object
    def route_error(self, error): 
        if error.broken_node != self.MY_ADDRESS:     
            self.routing_table.remove_route_from_table(error.broken_node.encode())
            print(error.broken_node + ' left!')
            if error.decrement_time_to_live() > 0:           
                self.writer.send_message(self.writer.add_separator(error))
                print('Error forwarded')
            else:
                del error
        else:
            del error

    # Compares received hash field to the ack_message_list table entries and deletes the matching entry.
    # @ack_message      Acknowledment message object 
    def ack_message(self, ack_message):
        if ack_message.destination == self.MY_ADDRESS:
            for key, value in list(self.ack_message_list.items()):
                if key == ack_message.hash_value.decode():                
                    self.lock()
                    del self.ack_message_list[key]
                    self.unlock()
                    UserInterface.print_outgoing_message(value.message.destination, value.message.payload)
        else:
            del ack_message

    # Forwards the received message if destination is not own address.
    # text_message    TextMessage object to be forwarded to next node.
    def forward_message(self, text_message, neighbor_node):
        if text_message.next_node == self.MY_ADDRESS and text_message.destination != self.MY_ADDRESS:
            if text_message.decrement_time_to_live() > 0:
                self.writer.send_message(self.writer.add_separator(RouteAck(self.MY_ADDRESS, 2, 5, neighbor_node, self.create_hash(text_message.source, text_message.payload))))              
                text_message.next_node = self.routing_table.find_route(text_message.destination) #finds the neighbor to destination
                self.ack_message_list[self.create_hash(text_message.source, text_message.payload)] = PendingMessage(text_message, 1)
                self.writer.send_message(self.writer.add_separator(text_message))
                print('Text message forwarded.') 
            else:
                del text_message
        elif text_message.next_node != self.MY_ADDRESS:
            del text_message
        elif text_message.destination == self.MY_ADDRESS and text_message.next_node == self.MY_ADDRESS:
            self.writer.send_message(self.writer.add_separator(RouteAck(self.MY_ADDRESS, 2, 5, neighbor_node, self.create_hash(text_message.source, text_message.payload))))
            UserInterface.print_incoming_message(text_message.source, text_message.payload)

    def create_hash(self, source, payload):    
        hashed = hashlib.md5(source + payload.encode()).hexdigest()
        return hashed[:6]

    # # Locks a code block for safely read from and write to a resource. 
    def lock(self):
        self.list_lock.acquire()

    # # releases a locked code block. 
    def unlock(self):
        self.list_lock.release()

    # Compares pending_message_list message destination to routing table destination entry for matches.
    # @return     list with matching messages list
    def get_pending_message_from_list(self):
        match = []
        for key in self.routing_table.table.keys():
            for entry in self.pending_message_list:
                if key == entry.message.destination.encode():
                    self.lock()
                    self.pending_message_list.remove(entry)
                    match.append(entry.message) 
                    self.unlock()     
        return match

    # Checks availablility of message destinations. If available they will be sent
    # otherwise retries will be counted up and the messages may be deleted. 
    def process_pending_user_message(self):
        match_list = self.get_pending_message_from_list()    
        if match_list:
            for message in match_list: 
                self.user_input(message)
                match_list.remove(message)
    
    # Removes all entries that have reached 3 retries.
    def clean_up_pending_message_list(self):
        if self.pending_message_list:
            for entry in self.pending_message_list:
                entry.retry += 1
                self.writer.send_message(self.writer.add_separator(RouteRequest(self.MY_ADDRESS, 3, 5, 0, entry.message.destination))) 
                if entry.retry == 3:
                    self.lock()
                    self.pending_message_list.remove(entry)
                    self.unlock()
                    print(entry.message.destination + ' is not available.')
        
    # Removes all entries that have reached 3 retries.
    def clean_up_ack_message_list(self):
        for key, value in list(self.ack_message_list.items()):
            value.retry +=1
            self.writer.send_message(self.writer.add_separator(value.message)) # sends the message again after each unsuccessful attempt.
            if value.retry == 3:
                self.writer.send_message(self.writer.add_separator(RouteError(self.MY_ADDRESS, 5, 5, value.message.destination)))
                self.lock()
                self.ack_message_list.pop(key.decode())
                self.unlock() 
                self.routing_table.remove_route_from_table(value.message.destination.encode())
                print(value.message.destination + ' left!')
                print('Error sent')
                

import threading, hashlib, time

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
        self.route_ack_list = dict()
        self.list_lock = threading.Lock()

    # Processes a message from user interface
    # @user_message    user message object.      
    def user_input(self, user_message):
        route = self.routing_table.find_route(user_message.destination)
        if not route:  
            self.writer.send_message(self.writer.add_separator(RouteRequest(self.MY_ADDRESS, 3, 5, 0, user_message.destination))) 
            self.pending_message_list.append(PendingMessage(user_message, self.get_time(), 1)) 
            print('Request sent')
        else:
            self.writer.send_message(self.writer.add_separator(TextMessage(self.MY_ADDRESS, 1, 5, user_message.destination, route.neighbor, user_message.message)))
            self.route_ack_list[self.create_hash(self.MY_ADDRESS, user_message.message)] = (PendingMessage(TextMessage(self.MY_ADDRESS, 1, 5, user_message.destination, route.neighbor, user_message.message), self.get_time(), 1))

    # Sends a request to all reachable nodes to find the requested node .
    # @request          Request message object.
    # @neighbor_node    Neighbor node address.       
    def route_request(self, request, neighbor_node):
        if request.source == self.MY_ADDRESS:
            return
        if request.requested_node == self.MY_ADDRESS: 
            if not self.routing_table.search_entry(request.source): 
                request.increment_hop()
                self.routing_table.add_route_to_table(request.source, neighbor_node, request.hop)     
            self.writer.send_message(self.writer.add_separator(RouteReply(self.MY_ADDRESS, 4, 5, 0, request.source, neighbor_node)))
            print('Reply sent')
            return
        if not self.routing_table.search_entry(request.source): 
            request.increment_hop()
            self.routing_table.add_route_to_table(request.source, neighbor_node, request.hop)
        if self.routing_table.search_entry(request.requested_node): 
            route = self.routing_table.find_route(request.requested_node) 
            if route:
                self.writer.send_message(self.writer.add_separator(RouteReply(route.destination, 4, 5, route.hop, request.source, neighbor_node)))
                print('Reply sent')
        else:
            if request.decrement_time_to_live() > 0:
                request.increment_hop()
                self.writer.send_message(self.writer.add_separator(request))
                print('Request forwarded')
                           
    # Processes reply messages
    # RouteReply(source, destination, flag, time_to_live, previous_node, end_node, metric))
    # reply            Reply message object.
    # neighbor_node    Neighbor node address.
    def route_reply(self, reply, neighbor_node):
        if reply.source == self.MY_ADDRESS or reply.next_node != self.MY_ADDRESS:
            return   
        if reply.next_node == self.MY_ADDRESS and reply.end_node == self.MY_ADDRESS: 
            if not self.routing_table.search_entry(reply.source):
                reply.increment_hop()
                self.routing_table.add_route_to_table(reply.source, neighbor_node, reply.hop)
                self.process_pending_user_message()             
        if reply.next_node == self.MY_ADDRESS and reply.end_node != self.MY_ADDRESS:
            if not self.routing_table.search_entry(reply.source):
                reply.increment_hop() 
                self.routing_table.add_route_to_table(reply.source, neighbor_node, reply.hop)
                if reply.decrement_time_to_live() > 0:  
                    route = self.routing_table.find_route(reply.end_node)
                    if route:  
                        reply.next_node = route.neighbor             
                        self.writer.send_message(self.writer.add_separator(reply))
                        print('Reply forwarded')
            
    # Processes a received error message. 
    # error    RouteError message object
    def route_error(self, error): 
        if error.broken_node != self.MY_ADDRESS:  
            if self.routing_table.search_entry(error.broken_node):
                self.routing_table.remove_route_from_table(error.broken_node)
                print(error.broken_node.decode() + ' left!')
                if error.decrement_time_to_live() > 0:           
                    self.writer.send_message(self.writer.add_separator(error))
                    print('Error forwarded')

    # Compares received hash field to the route_ack_list table entries and deletes the matching entry.
    # @ack_message      Acknowledment message object 
    def ack_message(self, ack_message):
        if ack_message.destination == self.MY_ADDRESS:
            self.lock()
            for key, value in list(self.route_ack_list.items()):
                if key == ack_message.hash_value.decode():                 
                    del self.route_ack_list[key]
                UserInterface.print_outgoing_message(value.message.destination, value.message.payload)
            self.unlock()       
        else:
            if ack_message.decrement_time_to_live() > 0:
                self.writer.send_message(self.writer.add_separator(ack_message))

    # Forwards the received message if destination is not own address.
    # @text_message    TextMessage object to be forwarded to next node.
    # @neighbor_node    Neighbor node address.   
    def forward_message(self, text_message, neighbor_node):
        if text_message.next_node == self.MY_ADDRESS and self.routing_table.search_entry(text_message.destination): 
            if text_message.destination != self.MY_ADDRESS:
                if text_message.decrement_time_to_live() > 0:
                    route = self.routing_table.find_route(text_message.destination)
                    if route:
                        text_message.next_node = route.neighbor
                        self.writer.send_message(self.writer.add_separator(text_message)) 
                        print('Message forwarded')
            else:
                if self.routing_table.search_entry(text_message.source):            
                    self.writer.send_message(self.writer.add_separator(RouteAck(self.MY_ADDRESS, 2, 5, text_message.source, self.create_hash(text_message.source, text_message.payload))))
                    UserInterface.print_incoming_message(text_message.source, text_message.payload)
    
    # creates a mad5 Hash value and return the first 6 characters.
    # @source      origin sender of the message.  
    # @payload     actual text message information.
    def create_hash(self, source, payload):    
        hashed = hashlib.md5(source + payload).hexdigest()
        return hashed[:6]

    # Function to get unixtime counting seconds since 1970.
    # int(time.time())     unix time in seconds since 1970
    def get_time(self):
        return int(time.time())

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
            self.lock()
            for entry in self.pending_message_list:
                if key == entry.message.destination:
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
    
    # Checks timestamps and removes all entries that have reached 3 retries.
    def clean_up_pending_message_list(self):
            self.lock()
            for entry in self.pending_message_list:
                if self.get_time() - entry.timestamp > 10.0:
                    entry.retry += 1
                    self.writer.send_message(self.writer.add_separator(RouteRequest(self.MY_ADDRESS, 3, 5, 0, entry.message.destination))) 
                    if entry.retry == 3:
                        self.pending_message_list.remove(entry)
                        print(entry.message.destination.decode() + ' is not available!!')
            self.unlock()
        
    # Checks timestamps and removes all entries that have reached 3 retries.
    def clean_up_route_ack_list(self):
        self.lock()
        for key, value in list(self.route_ack_list.items()):
            if self.get_time() - value.timestamp > 10.0:
                value.retry +=1
                self.writer.send_message(self.writer.add_separator(value.message)) # sends the message again after each unsuccessful attempt.
                if value.retry == 3:
                    self.writer.send_message(self.writer.add_separator(RouteError(self.MY_ADDRESS, 5, 5, value.message.destination)))               
                    self.route_ack_list.pop(key)   
                    self.routing_table.remove_route_from_table(value.message.destination)
                    print(value.message.destination.decode() + ' left!!')
                    print('Error sent')
        self.unlock() 
 
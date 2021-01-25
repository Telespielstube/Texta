import threading 

from RoutingTable import RoutingTable
from PendingMessage import PendingMessage
from RouteRequest import RouteRequest
from RouteReply import RouteReply
from RouteError import RouteError
from RouteAck import RouteAck
from TextMessage import TextMessage
from UserMessage import UserMessage
from UserInterface import UserInterface
from PendingMessageHandler import PendingMessageHandler
class MessageHandler:

    def __init__(self, MY_ADDRESS, routing_table, writer):
        self.MY_ADDRESS = MY_ADDRESS
        self.routing_table = routing_table
        self.writer = writer
        self.pending_message_handler = PendingMessageHandler()
        self.pending_message_handler.start()
    
    # Find a route to the request_message node
    # @request          Request message object.
    # @neigbor_node     previous node.
    def route_request(self, request, neighbor_node):
        if request.source == self.MY_ADDRESS and self.routing_table.search_entry(request.source):
            print('Request reached origin.')
        if request.requested_node == self.MY_ADDRESS:
            print('Request reached end node')
            if not self.routing_table.search_entry(request.source): 
                self.routing_table.add_route_to_table(request.source, neighbor_node, request.increment_hop())     
            self.writer.send_message(self.writer.message_to_string(RouteReply(self.MY_ADDRESS, 4, 9, 0, request.source, neighbor_node)))
        else:
            if not self.routing_table.search_entry(request.source): 
                self.routing_table.add_route_to_table(request.source, neighbor_node, request.increment_hop())
            if self.routing_table.search_entry(request.requested_node):  
                self.writer.send_message(self.writer.message_to_string(RouteReply(request.source, 4, 9, 0, request.source, neighbor_node)))
            elif request.decrement_time_to_live() > 0:  
                request.increment_hop()
                self.writer.send_message(self.writer.message_to_string(request))
                print('Request forwarded')
            else:
                print('ttl = 0. Request deleted')
                pass
    
    # Sends a reply to the source node if own address matches request_messageed node.
    # RouteReply(source, destination, flag, time_to_live, previous_node, end_node, metric))
    # reply            Reply message object.
    # neighbor_node    Neighbor node address.
    def route_reply(self, reply, neighbor_node):
        if reply.source == self.MY_ADDRESS and self.routing_table.search_entry(reply.source):
            print('Reply reached origin.') 
            pass   
        if reply.end_node == self.MY_ADDRESS and reply.next_node == self.MY_ADDRESS:
            print('Reply reached end node')
            if not self.routing_table.search_entry(reply.source):  
                self.routing_table.add_route_to_table(reply.source, neighbor_node, reply.increment_hop())              
        if reply.next_node == self.MY_ADDRESS and not self.routing_table.search_entry(reply.source) and not reply.end_node == self.MY_ADDRESS:
            self.routing_table.add_route_to_table(reply.end_node, neighbor_node, reply.increment_hop())
            if reply.decrement_time_to_live() > 0:              
                reply.increment_hop()    
                self.writer.send_message(self.writer.message_to_string(reply))
                print('Reply forwarded.')
            else: 
                print('ttl = 0 reply deleted')
                pass
        if reply.next_node != self.MY_ADDRESS:
            pass
           
    # Prepares the route message for sending. 
    # error    RouteError message object
    def route_error(self, error, neighbor_node):
        self.routing_table.remove_route_from_table(error.broken_node)          
        self.writer.send_message(self.writer.message_to_string(error))
        print('Route Error forwarded')

    # Forwards the received message if destination is not own address.
    # text_message    TextMessage to be forwarded to next node.
    def forward_message(self, text_message):
        if text_message.next_node == self.MY_ADDRESS and text_message.destination != self.MY_ADDRESS:
            if text_message.decrement_time_to_live() > 0:
                self.writer.send_message(self.writer.message_to_string(text_message))
                print('Text message forwarded.')
               # self.ack_message_list.append(text_message) 
        else:
            pass  
        if text_message.destination == self.MY_ADDRESS and text_message.next_node == self.MY_ADDRESS:
            UserInterface.print_incoming_message(text_message.source, text_message.payload)

    # Prepares the user text message for sending.
    # user_message    MessageItem object. Represents the user input.
    def text_message(self, user_message):
        self.writer.send_message(self.writer.message_to_string(user_message))

    # Message from user interface
    # @user_message    text message        
    def user_input(self, user_message):
        route = self.routing_table.find_route(user_message.destination)
        if not route:  
            self.writer.send_message(self.writer.message_to_string(RouteRequest(self.MY_ADDRESS, 3, 9, 0, user_message.destination))) 
            self.pending_message_handler.pending_message_list.append(PendingMessage(user_message, 1))
            print('Message is pending')
        else:
            self.text_message(TextMessage(self.MY_ADDRESS, 1, 9, user_message.destination, route, user_message.message))
            UserInterface.print_outgoing_message(user_message.destination, user_message.message)
            #selfpending_message_handler.ack_message_list(user_message)
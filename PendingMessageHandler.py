import threading, time, random

from Connection import Connection

class PendingMessageHandler(threading.Thread):

    def __init__(self):
        super(PendingMessageHandler, self).__init__()
        self.pending_message_list = []
        self.ack_message_list = []
        self.list_lock = threading.Lock()


    # Locks a code block for safely read from and write to it.
    def lock(self):
        self.list_lock.acquire()

    # releases a locked code block. 
    def unlock(self):
        self.list_lock.release()

    # Compares pending_message_list message destination and routing table destination esntry for matches.
    # @return     list with matching messages list
    def get_pending_message_from_list(self):
        match = []
        self.lock()
        for key in self.routing_table.table.keys():
            for entry in self.pending_message_list:
                if key == entry.message.destination.encode():
                    match.append(entry.message)
                else:
                    entry.message.retry += 1
        self.unlock()
        return match
    
    # Removes all entries that have reached 3 retries.
    def clean_up_pending_message_list(self):
        for entry in self.pending_message_list:
            if entry.retry == 3:
                del entry

    # Checks availablility of message destinations. If available they will be sent
    # otherwise retries will be counted up and the messages may be deleted. 
    def process_pending_user_message(self):
        match_list = self.get_pending_message_from_list()    
        if match_list:
            self.lock()
            for message in match_list:    
                self.user_input(self.pending_message_list.pop(message)) 
        self.clean_up_pending_message_list()
        self.unlock()
    
    # Regularily checks the acknowledgment list if an ack_msg was received.
    # If yes the message gets deleted an if not the message is sent again. 
    def process_ack_message(self):
        match = self.get_ack_message_from_list() 

    # Calculates a random int number between a minimum and maximum range.
    # @min   smallest number  
    # @max   largest number    
    def list_timer(self, min, max):
        return random.randint(min, max)

    def run(self):
        while True:
            time.sleep(self.list_timer(15, 25))
            self.message_handler.process_pending_user_message()
            #self.message_handler.process_ack_message()
            time.sleep(0.2)
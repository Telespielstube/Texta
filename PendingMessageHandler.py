import threading, time, random

from Connection import Connection

class PendingMessageHandler(threading.Thread):

    def __init__(self, message_handler):
        super(PendingMessageHandler, self).__init__()
        self.message_handler = message_handler

    # Calculates a random int number between a minimum and maximum range.
    # @min   smallest number  
    # @max   largest number    
    def list_timer(self, min, max):
        return random.randint(min, max)

    def run(self):
        while True:
            time.sleep(self.list_timer(15, 25))
            self.message_handler.process_pending_user_message()
           #print('Procees pending message')
            #check ack message list
            time.sleep(0.2)
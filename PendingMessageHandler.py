import threading, time, random

from Connection import Connection

class PendingMessageHandler(threading.Thread):

    def __init__(self, writer):
        super(PendingMessageHandler, self).__init__()
        self.writer = writer

    def list_timer(self, min, max):
        return random.randint(min, max)

    def run(self):
        while True:
            self.list_timer(15, 25)
            self.writer.process_pending_user_message()
           #print('Procees pending message')
            #check ack message list
            time.sleep(0.2)
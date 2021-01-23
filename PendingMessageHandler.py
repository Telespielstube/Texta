import threading, time

from Connection import Connection

class PendingMessageHandler(threading.Thread):

    def __init__(self, connection, writer):
        super(PendingMessageHandler, self).__init__()
        self.connection = connection
        self.writer = writer
        pass

    def run(self):
        while True:
            time.sleep(30)
            self.connection.lock()
            self.writer.process_pending_user_message()
            #check ack message list
            self.connection.unlock()
            time.sleep(0.3)
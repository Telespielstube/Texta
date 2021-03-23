import threading, time, random

from Connection import Connection

class PendingMessageTimer(threading.Thread):

    def __init__(self, message_handler):
        super(PendingMessageTimer, self).__init__()
        self.message_handler = message_handler

    def run(self):
        while True:
            time.sleep(10.0)
            if self.message_handler.pending_message_list:
                self.message_handler.clean_up_pending_message_list()
            if self.message_handler.route_ack_list:
                self.message_handler.clean_up_route_ack_list()

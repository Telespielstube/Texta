import threading
import queue
import time
from Connection import Connection

class Reader(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(self, Reader, Connection).__init__()
        self.communicate = Connection()
        self.name = name
        self.received_queue = queue.Queue()
        self.put_data_in_queue = ''

    def receive_data(self):
        self.put_data_in_queue = self.received_queue.put(str(self.communicate.readline().decode('utf-8')))
    
    def print_received_message(self, put_data_in_queue):
        message = received_queue.get(put_data_in_queue)
        print(message)
        
    def run(self):
        self.receive_data()
        self.print_received_message()
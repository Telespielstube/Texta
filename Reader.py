import threading
import queue
import time
from Connection import Connection
#from Parser import Parser
class Reader(threading.Thread):

    # Constructor for Reader class.
    # @group    reserved for future extension
    # @target   is the callable object to be invoked by the run() method.
    # @name     thread name
    # @args     is the argument tuple
    # @kwargs   is a dictionary of keyword arguments for the target invocation.
    # @verbose
    def __init__(self, thread_id, name, connection, read_lock):
        super(Reader, self).__init__()
        self.thread_id = thread_id
        self.name = name
        self.received_queue = queue.Queue()
        self.communicate = connection
        self.read_lock = read_lock
       # self.message = ''

    # Receives data from LoRa mcu and puts it in the queue.
    def receive_data(self):
        self.received_queue.put(self.communicate.read_from_mcu())
        self.received_queue.task_done()
        
        
    # Prints received data on screen.
    # @message    received data
    def print_received_message(self):
        for item in list(self.received_queue.queue):
            if '\r\n' in item:
                message = item.split('\r\n')
        print(message)
        
    def run(self):
        with self.read_lock:
            self.read_lock.wait_for(self.receive_data())
            self.receive_data()
        self.print_received_message()

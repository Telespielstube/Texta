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

             
    # Prints received data on screen.
    # @message    received data
    def print_received_message(self):
        for item in list(self.received_queue.queue):
            if '\r\n' in item:
                message = item.split('\r\n')
                print(message)
        
    def run(self):
        while True:
            self.received_queue.put(self.communicate.read_from_mcu())
            self.print_received_message()

import threading
import queue
import time
from Connection import Connection
#from Parser import Parser
class Reader(threading.Thread):
    lock = threading.Lock()

    # Constructor for Reader class.
    # @group    reserved for future extension
    # @target   is the callable object to be invoked by the run() method.
    # @name     thread name
    # @args     is the argument tuple
    # @kwargs   is a dictionary of keyword arguments for the target invocation.
    # @verbose
    def __init__(self, thread_id, name, connection):
        super(Reader, self).__init__()
        self.thread_id = thread_id
        self.name = name
        self.received_queue = queue.Queue()
        self.communicate = connection
        self.message = ''

    # Receives data from LoRa mcu and puts it in the queue.
    def receive_data(self):
        self.received_queue.put(self.communicate.read_from_mcu())
        if '\r\n' in self.received_queue:
            self.message = self.received_queue.split('\r\n')

    # Prints received data on screen.
    # @message    received data
    def print_received_message(self, message):
            print(message)
        
    def run(self):
        self.receive_data()
        with Reader.lock:
            self.print_received_message()
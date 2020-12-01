import threading
import queue
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
    # @message    received data decoded to utf-8
    def print_received_message(self, message):
        print(message.decode())  # or print(str(message, 'utf-8'))

    def run(self):
        while True:
            with self.read_lock: 
                message = self.communicate.read_from_mcu()
                self.received_queue.put(message)
            while not self.received_queue.empty:
                message = self.reaceived_queue.get()
                self.print_received_message(message)
       

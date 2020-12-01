import threading
import queue
import time

class Keyboard(threading.Thread):

    # Constructor for Reader class.
    # @group    reserved for future extension
    # @target   is the callable object to be invoked by the run() method.
    # @name     thread name
    # @args     is the argument tuple
    # @kwargs   is a dictionary of keyword arguments for the target invocation.
    # @verbose
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(Keyboard,self).__init__()
        self.name = name
        self.input_queue = queue.Queue()
        
    def read_console_input(self):
        command = input()
        self.input_queue.put(command)

    def run(self):
        while True:
            self.read_console_input()
           
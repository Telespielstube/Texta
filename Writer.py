import threading
import time
import queue
from Keyboard import Keyboard
from Connection import Connection

class Writer(threading.Thread):

    # Constructor for Reader class.
    # @group    reserved for future extension
    # @target   is the callable object to be invoked by the run() method.
    # @name     thread name
    # @args     is the argument tuple
    # @kwargs   is a dictionary of keyword arguments for the target invocation.
    # @verbose
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(Writer,self).__init__()
        self.name = name
        self.keyboard = Keyboard()
        self.communicate = Connection()
        self.transmit_queue = queue.Queue()

    #def message_builder(self):
    
    def trasmit_data(self, message):
        message += message + '\n\r'
        byte_message = bytes(message, 'utf-8')
        self.communicate.write_to_mcu(byte_message)
    
    def run(self):  
        if not self.keyboard.input_queue.empty():
            message = self.keyboard.input_queue.get()
            self.trasmit_data(message)
        else:
            message = self.transmit_queue.get()
            self.trasmit_data(message)
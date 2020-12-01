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
    def __init__(self, thread_id, name, connection, write_lock, keyobard):
        super(Writer,self).__init__()
        self.thread_id = thread_id
        self.name = name
        self.communicate = connection
        self.write_lock = write_lock
        self.keyboard = keyboard
        self.transmit_queue = queue.Queue()
    
    def trasmit_data(self, message):
        message += message + '\r\n'
        byte_message = bytes(message, 'utf-8')
        self.communicate.write_to_mcu(byte_message)
    
    def run(self): 
        for item in list(self.transmit_queue.queue):
            with self.write_lock:
                self.transmit_data(item)
        # for item in list(self.keyboard.input_queue.queue):
        #     with self.write_lock:
        #         self
        # if not self.keyboard.input_queue.empty():
        #     message = self.keyboard.input_queue.get()
        #     with self.write_lock:
        #         self.trasmit_data(message)
        # else:
        #     message = self.transmit_queue.get()
        #     with self.write_lock:
        #         self.trasmit_data(message)
import threading
import time
import queue
from Keyboard import Keyboard
from Connection import Connection

class Writer(threading.Thread):
    event = threading.Event()
    # Constructor for Writer class.
    # @thread_id
    # @name
    # @connection
    # @write_lock
    # @keyboard
    def __init__(self, thread_id, name, connection, write_lock, keyboard):
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
                Writer.event.wait(2)
                
 

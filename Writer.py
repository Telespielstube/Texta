import threading
import queue
import time

from Keyboard import Keyboard
from Connection import Connection
#from Parser import Parser
#from Header import Header

class Writer(threading.Thread):
    HEADER_LENGTH = 14
    MY_ADDRESS = '0136'

    # Constructor for Writer class.
    # @thread_id    thread id
    # @name         thread name
    # @connection   connection to the serial device
    # @write_lock   locks the writing process to the mcu
    def __init__(self, thread_id, name, connection):
        super(Writer,self).__init__()
        self.thread_id = thread_id
        self.name = name
        self.communicate = connection
        self.transmit_queue = queue.Queue()
        #self.parser = Parser(connection)
    
    def run(self): 
        while True:
            if self.transmit_queue.empty():
                time.sleep(0.5)
            while not self.transmit_queue.empty():
                message = self.transmit_queue.get()     
                self.communicate.write_to_mcu(message)
                self.transmit_queue.task_done()
             


           

            
            

 

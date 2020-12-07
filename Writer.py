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
    def __init__(self, thread_id, name, connection, write_lock):
        super(Writer,self).__init__()
        self.thread_id = thread_id
        self.name = name
        self.communicate = connection
        self.write_lock = write_lock
        self.transmit_queue = queue.Queue()
        #self.parser = Parser(connection)

    def stopwatch(self, seconds):
        start_time =time.time()
        elapsed_time = 0
        while elapsed_time < seconds:
            elapsed_time = time.time() - start_time 
        return elapsed_time

    def hello_paket(self, message):
       self.transmit_queue.put(message)

    def auto_msg(self, message):
        self.transmit_queue.put(message)

    def run(self): 
        while True:
            if self.transmit_queue.empty():
                time.sleep(0.5)
            while not self.transmit_queue.empty():
                message = self.transmit_queue.get() 
                with self.write_lock:
                    self.communicate.write_to_mcu(message)
            
            if self.stopwatch() < 10:
                self.hello_paket('AT+SEND=15')
                self.hello_paket('Hello from 0136')
            elif self.stopwatch() < 20:
                self.auto_msg('AT+SEND=27')
                self.auto_msg('Heute ist der 10. Dezember.' )

            
            

 

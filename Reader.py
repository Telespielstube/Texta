import threading
import time
import queue

from Connection import Connection
#from Parser import Parser
class Reader(threading.Thread):

    # Constructor for Reader class.
    # @thread_id    thread id
    # @name         thread name
    # @connection   connection to the serial device
    # @read_lock   locks the writing process to the mcu
    def __init__(self, thread_id, name, connection):
        super(Reader, self).__init__()
        self.thread_id = thread_id
        self.name = name
        self.receive_queue = queue.Queue()
        self.communicate = connection
        #self.parser = Parser(connection)
            
    # Prints received data on screen.
    # @message    received data encoded to utf-8
    def print_received_message(self, message):
        print(message.decode().rstrip('\r\n'))

    # Overridden Thread function to execute functions necessary to read from mcu.
    def run(self):
        # constantly read from mcu, if received message is empty 
        # sleep if message has content break from if statement and put message to queue
        while True:
            message = self.communicate.read_from_mcu()
            if not message:
                time.sleep(0.01)                          
            else:
                break
            self.receive_queue.put(message)

            while not self.receive_queue.empty():
                message = self.receive_queue.get()
                self.receive_queue.task_done()
                self.print_received_message(message)
               # self.parser.parse_message(message)

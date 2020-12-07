import threading
import queue
from Connection import Connection
#from Parser import Parser
class Reader(threading.Thread):

    # Constructor for Reader class.
    # @thread_id    thread id
    # @name         thread name
    # @connection   connection to the serial device
    # @read_lock   locks the writing process to the mcu
    def __init__(self, thread_id, name, connection, read_lock):
        super(Reader, self).__init__()
        self.thread_id = thread_id
        self.name = name
        self.received_queue = queue.Queue()
        self.communicate = connection
        self.read_lock = read_lock
        #self.parser = Parser(connection)
            
    # Prints received data on screen.
    # @message    received data decoded to utf-8
    def print_received_message(self, message):
        print(message.decode())

    def run(self):
        while True:
            with self.read_lock: 
                message = self.communicate.read_from_mcu()
                self.received_queue.put(message)
            while not self.received_queue.empty():
                message = self.received_queue.get()
                self.print_received_message(message)
               # self.parser.parse_incoming_message(message)

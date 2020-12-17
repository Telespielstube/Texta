import threading
import time
import queue

from Connection import Connection
from Parser import Parser
class Reader(threading.Thread):

    # Constructor for Reader class.
    # @thread_id    thread id
    # @name         thread name
    # @connection   connection to the serial device
    # @read_lock   locks the reading process to the mcu
    def __init__(self, thread_id, name, connection, parser):
        super(Reader, self).__init__()
        self.thread_id = thread_id
        self.name = name
        self.receive_queue = queue.Queue()
        self.communicate = connection
        self.parser = parser
            
    # Prints received data on screen.
    # @message    received data encoded to utf-8
    def print_received_message(self, message):
        print(message.decode())
    
    def slice_incoming_message(self, message):
        mcu_header = message[:11]
        own_header = message[11:21]
        payload = message[21:]
        return mcu_header, own_header, payload 

    # Overridden Thread function to execute functions necessary to read from mcu.
    def run(self):
        # constantly read from mcu, if received message is empty 
        # sleep if message has content break from if statement and put message to queue
        while True:
            message = self.communicate.read_from_mcu()
            if not message:
                time.sleep(0.2)
                continue
            self.receive_queue.put(message)

            while not self.receive_queue.empty():
                message = self.receive_queue.get()
                mcu_header, own_header, payload = self.slice_incoming_message(message)
                self.receive_queue.task_done()
                self.print_received_message(payload)
                self.parser.parse_incoming_message(mcu_header, own_header)

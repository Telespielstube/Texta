import threading
import queue
import time

class Automator(threading.Thread):

    def __init__(self, thread_id, name, writer):
        super(Automator, self).__init__()
        self.thread_id = thread_id
        self.name = name
        self.writer = writer

    def hello_packet(self, *arguments):
        for argument in arguments:
            self.writer.transmit_queue.put(argument)
        print(argument)

    # Overridden Thread function to execute functions necessary to send automated messages at intervalls to mcu.
    def run(self):
        while True:
            time.sleep(10)
            self.hello_packet('AT+SEND=15', 'Hello from 0136')
            
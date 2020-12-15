import threading
import queue
import time
from MessageItem import MessageItem

class Automator(threading.Thread):

    def __init__(self, thread_id, name, writer):
        super(Automator, self).__init__()
        self.thread_id = thread_id
        self.name = name
        self.writer = writer
    
    def auto_msg(self, *arguments):
        write_queue_item = MessageItem(arguments[0], arguments[1], arguments[2])
        self.writer.transmit_queue.put(write_queue_item)

    # Overridden Thread function to execute functions necessary to send automated messages at intervalls to mcu.
    def run(self):
        while True:
            time.sleep(10)
            self.auto_msg('SEND', 'Hello from 0136', 'FFFF')
            #self.auto_msg('SEND', 'Hello from 0136', 'FFFF')
            # time.sleep(30)
            # self.auto_msg('AT+DEST=FFFF', 'AT+SEND=74', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.')
            
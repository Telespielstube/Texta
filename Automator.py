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
        write_message_item = MessageItem(arguments[0], arguments[1], arguments[2])
        print(write_message_item.command + ', '+ write_message_item.message + ', ' + write_message_item.destination)
        self.writer.transmit_queue.put(write_message_item)

    # Overridden Thread function to execute functions necessary to send automated messages at intervalls to mcu.
    def run(self):
        self.auto_msg('SEND', 'Hello from 0136', '0136')
        while True:
            time.sleep(15)
            self.auto_msg('SEND', 'Hello from 0136', '0136')
            time.sleep(25)
            self.auto_msg('SEND', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.', '0136')
            
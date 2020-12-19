import threading
import queue
import time

from MessageItem import MessageItem

class Automator(threading.Thread):

    def __init__(self, writer, header):
        super(Automator, self).__init__()
        self.writer = writer
        self.header = header
    
    def auto_msg(self, *arguments):
        write_message_item = MessageItem(arguments[0], arguments[1], arguments[2])
        print(write_message_item.command + ' '+ write_message_item.message + ' ' + write_message_item.destination)
        self.header.flag = 0
        print (self.header.flag)
        self.header.time_to_live = 1
        print (self.header.time_to_live)
        self.writer.transmit_queue.put(write_message_item)

    # Overridden Thread function to execute functions necessary to send automated messages at intervalls to mcu.
    def run(self):
        time.sleep(6)
        self.auto_msg('SEND', 'Hello from 0136', '0139')
        while True:
            time.sleep(55)
            self.auto_msg('SEND', 'Hello from 0136', '0139')
            

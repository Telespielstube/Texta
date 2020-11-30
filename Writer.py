import threading
import time
import queue
from Keyboard import Keyboard
from Connection import Connection

class Writer(threading.Thread, Keyboard):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(Writer,self).__init__()
        self.name = name
        self.keyboard = Keyboard()
        self.communicate = Connection()

    #def message_builder(self):

    def trasmit_data(self, message):
        byte_message = bytes(message, 'utf-8')
        self.communicate.write(byte_message)
    
    def run(self):  
        if self.keyboard.input_queue.empty():
            pass
        else:
            message = self.keyboard.input_queue.get()
            self.trasmit_data(message)


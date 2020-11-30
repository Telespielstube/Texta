import threading
import time
import queue
from Keyboard import Keyboard
from Communication import Communication

class Writer(threading.Thread, Keyboard):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(Writer,self, keyboard).__init__()
        self.name = name
        self.keyboard = keyboard

    def trasmit_data(self):
        message = self.keyboard.get()
        byte_message = bytes(message, 'utf-8')
    def run(self):  


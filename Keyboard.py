import threading
import queue
import time

class Keyboard(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(Keyboard,self).__init__()
        self.name = name
        self.input_queue = queue.Queue()
        
    def read_console_input(self):
        while True:
            command = input()
            self.input_queue.put(command)

    def run(self):
        while True:
            self.read_console_input()
           
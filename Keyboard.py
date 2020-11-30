import threading
import queue
import time

class Keyboard(threading.Thread):

    input_queue = queue.Queue() # global variable

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(Keyboard,self).__init__()
        self.name = name

    def read_console_input(self):
        while True:
            command = input()
            Keyboard.input_queue.put(command)

    def run(self):
        while True:
            self.read_console_input()
           
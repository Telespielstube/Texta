import threading
from Writer import Writer
from Reader import Reader
from Keyboard import Keyboard

class ThreadHandler():

    def __init__(self, connection):
        self.thread_lock = threading.Lock()
        self.writer = Writer(1, 'writer', connection, thread_lock)
        self.reader = Reader(2, 'reader', connection, thread_lock)
        self.keyboard = Keyboard(3, 'keybaord')
        self.start_threads()
        

    def start_threads(self):
        while True:
            self.writer.start()
            self.reader.start()
            self.keyboard.start()
            self.writer.join()
            self.reader.join()
            self.keyboard.join()
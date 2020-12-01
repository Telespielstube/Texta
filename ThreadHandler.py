import threading
from Writer import Writer
from Reader import Reader
from Keyboard import Keyboard

class ThreadHandler():

    def __init__(self, connection):
        self.writer = Writer(1, 'writer', connection)
        self.reader = Reader(2, 'reader', connection)
        self.keyboard_input = Keyboard(name='keybaord')
        self.start_threads()

    def start_threads(self):
        while True:
            self.writer.start()
            self.reader.start()
            self.writer.join()
            self.reader.join()
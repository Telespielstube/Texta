import threading
from Writer import Writer
from Reader import Reader
from Keyboard import Keyboard

class ThreadHandler():

    def __init__(self, connection):
        self.writer = Writer(name='writer', target=writer, args=(connection,))
        self.reader = Reader(name='reader', target=reader, args=(connection,))
        self.keyboard_input = Keyboard(name='keybaord')
        self.start_threads()

    def start_threads(self):
        while True:
            self.writer.start()
            self.reader.start()
            self.writer.join()
            self.reader.join()
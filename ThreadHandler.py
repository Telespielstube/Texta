import threading
from Writer import Writer
from Reader import Reader
from Keyboard import Keyboard

class ThreadHandler():

    def __init__(self):
        self.writer = Writer(name='writer')
        self.reader = Reader(name='reader')
        self.keyboard_input = Keyboard(name='keybaord')
        self.start_threads()

    def start_threads(self):
        #self.writer.start()
        self.reader.start()
import threading
from Writer import Writer
from Reader import Reader
from Keyboard import Keyboard

class ThreadHandler():

    def __init__(self, connection):
        self.thread_lock = threading.Lock()
        self.keyboard = Keyboard(3, 'keybaord')
        self.writer = Writer(1, 'writer', connection, self.thread_lock, self.keyboard)
        self.reader = Reader(2, 'reader', connection, self.thread_lock)


    #  self.keyboard.start()
    self.writer.start()
    self.reader.start()
    
    self.writer.join()
    self.reader.join()
    # self.keyboard.join()
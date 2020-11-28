import threading
import time

class Reader:

    def __init__(self, name=None):
        super(Reader,self).__init__()
        self.name = name
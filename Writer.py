import threading
import time

class Writer:

    def __init__(self, name=None):
        super(Writer,self).__init__()
        self.name = name
        

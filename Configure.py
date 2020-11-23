import serial
import threading
from time import sleep

class Configure:

    def __init__(self, communicate):
        self.communicate = communicate

    """ Constructor """
    def config_modul(self, *args):
        for arg in args:
            self.communicate.write(str(arg).encode("UTF-8"))
            sleep(3)


    


        
        

    





      

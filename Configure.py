import serial
import threading
import logging
from time import sleep

class Configure:

    logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)
    
    def __init__(self, communicate):
        self.communicate = communicate

    """ Constructor """
    def config_modul(self, *args):
        for arg in args:
            message = arg + "\r\n"
            byte_message = bytes(message, 'utf-8')
            self.communicate.write(byte_message)
            print(arg)
            read = str(self.communicate.readline().decode("utf-8"))
            print(stripped)
            sleep(3)


    

        
        

    





      

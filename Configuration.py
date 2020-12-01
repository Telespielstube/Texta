import serial
from Writer import Writer
import queue
class Configuration:
    
    def __init__(self, writer):
        self.writer = writer

    # Configures the Lora module
    def config_modul(self, args):
        print(argument)
        self.writer.transmit_queue.put(argument)
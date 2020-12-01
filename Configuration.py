import serial
from Writer import Writer
import queue
class Configuration:
    
    def __init__(self, writer, connection):
        self.writer = writer
        self.connection = connection

    # Configures the Lora module
    def config_modul(self, argument):
        print(argument)
        self.connection.write_to_mcu(argument)
import serial
import time

from Writer import Writer
from Connection import Connection
class Configuration:
    
    def __init__(self, writer, connection):
        self.writer = writer
        self.connection = connection

    # Configures the Lora module
    def config_module(self, *arguments):
        for argument in arguments:
            print(argument)
            self.connection.write_to_mcu(argument)
            time.sleep(1.0)
            message = self.connection.read_from_mcu()
            print(message.decode())

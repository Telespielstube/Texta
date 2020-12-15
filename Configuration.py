import serial
import time

from Connection import Connection
class Configuration:
    
    def __init__(self, connection):
        self.connection = connection

    # Configures the Lora module
    def config_module(self, *arguments):
        for argument in arguments:
            self.connection.write_to_mcu(argument)
            time.sleep(1)       
            message = self.connection.read_from_mcu()    
            print(message.decode())

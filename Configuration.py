import serial
import time

from Connection import Connection
class Configuration:
    
    def __init__(self, connection):
        self.connection = connection

    # Configures the Lora module
    def config_module(self, *arguments):
        for argument in arguments:
            print(argument)
            self.connection.write_to_mcu(argument)
            time.sleep(1)
            # constantly read from mcu, if received message is empty 
            # sleep if message has content break from if statement and print message         
            message = self.connection.read_from_mcu()    
            print(message.decode())

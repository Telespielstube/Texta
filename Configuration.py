import serial
import time

from Connection import Connection
class Configuration:
    
    def __init__(self, connection):
        self.connection = connection

    # Configures the Lora module
    def config_module(self, *arguments):
        self.connection.write_to_mcu(arguments[0])
        for i in range(0, 1):        
            time.sleep(1)
            validation = self.connection.read_from_mcu()
            print(validation[:-1].decode())
        for i in range(1, len(arguments)):
            self.connection.write_to_mcu(arguments[i])
            time.sleep(1.5)       
            validation = self.connection.read_from_mcu()
            print(validation[:-1].decode())

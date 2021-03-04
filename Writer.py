import time, random

from Connection import Connection

class Writer():

    # Constructor for Writer class.
    # @connection       connection to the serial device
    # @header           
    # @configuration    
    def __init__(self, connection):
        super(Writer, self).__init__()
        self.connection = connection

    # Calculates a random floating number between a minimum and maximum range.
    # @min       smallest number  
    # @max       largest number    
    # @return    random number.
    def waiting_time(self, min, max):
        return random.uniform(min, max)

    # Converts all different data types of the message to string and adds the field seperator.
    # @message    ields of the message  
    def add_separator(self, message): 
        separator = '|'
        separated_message = ''
        for attr, value in message.__dict__.items():
            if type(value) == bytes:
                value = value.decode() 
            separated_message += str(value) + separator
        return separator + separated_message 

    # Prepares the message for sending to the write_to_mcu function.
    # @message      holds all specific fields the message object has
    def send_message(self, message):
        time.sleep(self.waiting_time(0.1, 0.4))
        self.connection.lock()
        command_string = 'AT+SEND='
        command_string += str(len(message))
        self.connection.write_to_mcu(command_string)
        time.sleep(1)
        self.connection.read_from_mcu()
        self.connection.write_to_mcu(message)
        time.sleep(1)
        self.connection.read_from_mcu()
        self.connection.unlock()                

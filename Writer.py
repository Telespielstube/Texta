import threading, time 

from Connection import Connection

class Writer():

    # Constructor for Writer class.
    # @connection       connection to the serial device
    # @header           
    # @configuration    
    def __init__(self, connection):
        self.connection = connection

    # Converts all different data types of the message to string and adds the field seperator.
    # @message    ields of the message  
    def message_to_string(self, message): 
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

    

                
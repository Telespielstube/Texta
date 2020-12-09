import serial
import threading

class Connection: 
  
    def __init__(self, port, baudrate, bytesize, parity, stopbits, timeout):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = None
        self.serial_connection = None
        self.access_lock = threading.Lock()

    # Connects to the Lora mcu.
    def connect_device(self):  
        self.serial_connection = serial.Serial(self.port, self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout)
        return self.serial_connection

    # Closes connection to serial device
    def close_connection(self):
        self.serial_connection.close()

    # Writes data to the serial device
    # @message  data to send
    def write_to_mcu(self, message):
        with self.access_lock:
            message = message + '\r\n'
            byte_message = message.encode()
            self.serial_connection.write(byte_message)

    # Reads data from the serical device
    def read_from_mcu(self):
        with self.access_lock:
            message = self.serial_connection.readline()
            return message
        
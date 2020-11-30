import serial

class Connection: 
        
    def __init__(self, port=None, baudrate=None, bytesize=None, parity=None, stopbits=None, timeout=None):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.serial_connection = None

    # Connects to the Lora mcu.
    def connect_device(self, port, baudrate, bytesize, parity, stopbits, timeout):  
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout)
            print('Port: ' + self.ser.name) 
        except IOError:
            print("Port already open or anything else went wrong.")
        
        return self.serial_connection

    def close_Connection(self):
        self.serial_connection.close()

    def write_to_mcu(self, message):
        self.serial_connection.write(message)

    def read_from_mcu(self):
        read = self.serial_connection.readline.decode('utf-8')
        return str(read)
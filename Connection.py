import serial

class Connection: 
  
    def __init__(self, port, baudrate, bytesize, parity, stopbits, timeout):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.serial_connection = None

    # Connects to the Lora mcu.
    def connect_device(self):  
        self.serial_connection = serial.Serial(self.port, self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout)
        print('Port: ' + self.serial_connection.name) 
        return self.serial_connection

    def close_Connection(self):
        self.serial_connection.close()

    def write_to_mcu(self, message):
        self.serial_connection.write(message)

    def read_from_mcu(self):
        message = self.serial_connection.readline()
       # print(message.decode('utf-8').split(b'\r\n'))
        print(str(message, 'utf-8'))
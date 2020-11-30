import serial

class Connection: 
        
    def __init__(self):
        self.ser 

    # Connects to the Lora mcu.
    def connect_device(self, port, baudrate, bytesize, parity, stopbits, timeout):  
        try:
            self.ser = serial.Serial(self.port, self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout)
            print('Port: ' + self.ser.name) 
        except IOError:
            print("Port already open or anything else went wrong.")
        
        return self.ser

    def write_to_mcu(self, message):
        self.ser.write(message)

    def read_from_mcu(self, message):
        read = str(self.ser.readline.decode('utf-8'))
        return read
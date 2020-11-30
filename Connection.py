import serial

class Connection: 
        
    def __init__(self):
        self.ser = None

    # Connects to the Lora mcu.
    def connect_device(self, port, baudrate, bytesize, parity, stopbits, timeout):  
        try:
            self.ser = serial.Serial(port, baudrate, bytesize, parity, stopbits, timeout)
            print('Port: ' + self.ser.name) 
        except IOError:
            print("Port already open or anything else went wrong.")
        
        return self.ser

    def write_to_mcu(self, message):
        self.ser.write(message)

    def read_from_mcu(self):
        read = self.ser.readline.decode('utf-8')
        return str(read)
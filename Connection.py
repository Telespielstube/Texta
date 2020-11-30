import serial

class Connection: 
        
    def __init__(self, port, baudrate, bytesize, parity, stopbits, timeout):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout

    def connect_device(self):
        self.ser = 0
        try:
            self.ser = serial.Serial(self.port, self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout)
            print('Port: ' + self.ser.name) 

        except IOError:
            print("Port already open or anything else went wrong.")
        
        return self.ser


                

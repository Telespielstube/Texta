from serial import Serial

class Connect: 
        
    def __init__(self, port, baudrate, bytesize, parity, stopbits, timeout):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout

    def connect_device(self):
        self.serial = 0
        try:
            self.serial = Serial(self.port, self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout)
            self.serial.write(b'Port: ' + str(self.port).encode("UTF-8")) 

        except IOError:
            print("Port already open or anything else went wrong.")
        
        return self.serial


                
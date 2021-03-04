import serial, threading

class Connection: 
  
    def __init__(self, port, baudrate, bytesize, parity, stopbits, timeout):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.serial_connection = None
        self.access_lock = threading.Lock()

    # Connects to the Lora mcu.
    def connect_device(self):  
        self.serial_connection = serial.Serial(self.port, self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout)
        return self.serial_connection

    # Closes connection to serial device
    def close_connection(self):
        self.serial_connection.close()

    # Adding carriage return and writes data to the serial device 
    # @message      data to send
    def write_to_mcu(self, message):
        #print('Writer: ' + message)
        self.serial_connection.write((message + '\r\n').encode())

    # Reads data from the serial device
    def read_from_mcu(self):
        return self.serial_connection.readline()

    # activates a lock to safely read / write to the lora modul   
    def lock(self):
        self.access_lock.acquire()

    # deactivates the read / write access
    def unlock(self):
        self.access_lock.release()

import threading

from Connection import Connection 
from Configuration import Configuration    
from Writer import Writer
from Reader import Reader
from Keyboard import Keyboard

def main():
   # Connecting to LoRa mcu.
   # connection = Connection('/dev/ttyS0', 115200, 8, 'N', 1, 2)
    connection = Connection('/dev/ttys003', 115200, 8, 'N', 1, 2)
    connection.connect_device()

    #Setting up threads
    thread_lock = threading.Lock()
    writer = Writer(2, 'writer', connection, thread_lock)
    keyboard = Keyboard(1, 'keyboard', writer)
    reader = Reader(3, 'reader', connection, thread_lock)
    
    #Configuring the mcu
    configure = Configuration(writer, connection)
    configure.config_module('AT+RST')
    configure.config_module('AT+CFG=433500000,20,6,12,1,1,0,0,0,0,3000,8,4')
    configure.config_module('AT+ADDR=0136')
    configure.config_module('AT+DEST=FFFF')
    configure.config_module('AT+RX')
    configure.config_module('AT+SAVE')

    # Starting the threads
    writer.start()
    reader.start()
    keyboard.start()

if __name__ == '__main__':
    main()


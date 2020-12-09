import threading

from Connection import Connection 
from Configuration import Configuration    
from Writer import Writer
from Reader import Reader
from Keyboard import Keyboard
from Automator import Automator

def main():
   # Connecting to LoRa mcu.
   # connection = Connection('/dev/ttyS0', 115200, 8, 'N', 1, 2)
    connection = Connection('/dev/ttys006', 115200, 8, 'N', 1, 2)
    connection.connect_device()

    #Setting up threads
    writer = Writer(1, 'writer', connection)
    reader = Reader(2, 'reader', connection)
    keyboard = Keyboard(3, 'keyboard', writer)
    automator = Automator(4, 'automator', writer)
    
    #Configuring the mcu
    configure = Configuration(writer, connection)
    configure.config_module('AT+RST', 'AT+CFG=433500000,20,6,12,1,1,0,0,0,0,3000,8,4', 
                            'AT+ADDR=0136',
                            'AT+DEST=FFFF',
                            'AT+RX',
                            'AT+SAVE')

    # Starting the threads
    writer.start()
    reader.start()
    keyboard.start()
    automator.start()

if __name__ == '__main__':
    main()


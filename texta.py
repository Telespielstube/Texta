import threading
import time
from Connection import Connection 
from Configure import Configure    
from Writer import Writer
from Reader import Reader
from Keyboard import Keyboard

def main():
    #Creates three thread Objects and starts them.
    writer = Writer(name='writer')
    reader = Reader(name='reader')
    keyboard_input = Keyboard(name='keybaord')

    # Connecting and setting up the LoRa mcu.
    connect = Connect('/dev/ttyS0', 115200, 8, 'N', 1, 1)
    communicate = connect.connect_device()
    configure = Configure(communicate)
    configure.config_modul('AT+RST',
                        'AT+CFG=433000000,20,6,12,1,1,0,0,0,0,3000,8,4',
                        'AT+ADDR=0136',
                        'AT+RX',
                        'AT+SAVE')

if __name__ == '__main__':
    main()



      


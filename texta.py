#from ThreadHandler import ThreadHandler
import threading
from Connection import Connection 
from Configuration import Configuration    
from Writer import Writer
from Reader import Reader
from Keyboard import Keyboard

def main():
     #Setting up threads
    thread_lock = threading.Lock()
    keyboard = Keyboard(3, 'keyboard')
    writer = Writer(1, 'writer', connection, thread_lock, keyboard)
    reader = Reader(2, 'reader', connection, thread_lock)
    
    # Connecting to LoRa mcu.
    connection = Connection('/dev/ttyS0', 115200, 8, 'N', 1, 1)
    connection.connect_device()

    configure = Configuration(writer)
    configure.config_modul('AT+RST')
    configure.read_from_mcu()
    configure.config_modul('AT+CFG=433000000,20,6,12,1,1,0,0,0,0,3000,8,4')
    configure.read_from_mcu()
    configure.config_modul('AT+ADDR=0136')
    configure.read_from_mcu()
    configure.config_modul('AT+RX')
    configure.read_from_mcu()
    configure.config_modul('AT+SAVE')
    configure.read_from_mcu()

   

    writer.start()
    reader.start()

if __name__ == '__main__':
    main()



      


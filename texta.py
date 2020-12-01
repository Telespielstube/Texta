#from ThreadHandler import ThreadHandler
import threading
from time import sleep
from Connection import Connection 
from Configuration import Configuration    
from Writer import Writer
from Reader import Reader
from Keyboard import Keyboard

def main():
   # Connecting to LoRa mcu.
    connection = Connection('/dev/ttyS0', 115200, 8, 'N', 1, 2)
    connection.connect_device()
    #Setting up threads
    thread_lock = threading.Lock()
    writer = Writer(2, 'writer', connection, thread_lock)
    keyboard = Keyboard(1, 'keyboard', writer)
    reader = Reader(3, 'reader', connection, thread_lock)
    #Configuring the mcu
    configure = Configuration(writer, connection)
    configure.config_modul('AT+RST')
    configure.config_modul('AT+CFG=433000000,20,6,12,1,1,0,0,0,0,3000,8,4')
    configure.config_modul('AT+ADDR=0136')
    configure.config_modul('AT+RX')
    configure.config_modul('AT+SAVE')
    # Starting the threads
    writer.start()
    reader.start()
    keyboard.start()
    writer.join()
    reader.join()
    keyboard.join()
if __name__ == '__main__':
    main()



      


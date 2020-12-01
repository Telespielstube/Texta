from ThreadHandler import ThreadHandler
from Connection import Connection 
from Configuration import Configuration    

def main():

    # Connecting to LoRa mcu.
    connect = Connection('/dev/ttyS0', 115200, 8, 'N', 1, 1)
    connect.connect_device()

    #Setting up threads
    thread_lock = threading.Lock()
    keyboard = Keyboard(3, 'keybaord')
    writer = Writer(1, 'writer', connection, self.thread_lock, self.keyboard)
    reader = Reader(2, 'reader', connection, self.thread_lock)

    writer.start()
    configure = Configuration(writer)
    configure.config_modul('AT+RST', 'AT+CFG=433000000,20,6,12,1,1,0,0,0,0,3000,8,4', 'AT+ADDR=0136', 'AT+RX', 'AT+SAVE')
    reader.start()
    
    writer.join()
    reader.join()
    
    # thread_handler = ThreadHandler(connect)
    

if __name__ == '__main__':
    main()



      


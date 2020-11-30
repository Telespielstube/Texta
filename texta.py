from ThreadHandler import ThreadHandler
from Connection import Connection 
from Configuration import Configuration    

def main():
    thread_handler = ThreadHandler()
    # Connecting and setting up the LoRa mcu.
    connect = Connection()
    connect.connect_device('/dev/ttyS0', 115200, 8, 'N', 1, 1)
    
    configure = Configuration()
    configure.config_modul('AT+RST',
                        'AT+CFG=433000000,20,6,12,1,1,0,0,0,0,3000,8,4',
                        'AT+ADDR=0136',
                        'AT+RX',
                        'AT+SAVE')

if __name__ == '__main__':
    main()



      


from Connect import Connect 
from Configure import Configure    

""" Setting up the module. """ 
connect = Connect('/dev/ttys003', 115200, 8, 'N', 1, 1)
communicate = connect.connect_device()
configure = Configure(communicate)
configure.config_modul('AT+RST',
                       'AT+CFG=433000000,20,6,12,1,1,0,0,0,0,3000,8,4',
                       'AT+ADDR=2702',
                       'AT+RX',
                       'AT+SAVE')





      


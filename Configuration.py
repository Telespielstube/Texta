import serial
from Writer import Writer
import queue
class Configuration:

    logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)
    
    def __init__(self, communicate):
        self.communicate = communicate
        self.writer = Writer()

    # Constructor
    def config_modul(self, *args):
        for argument in args:
            print(argument)
            message = argument + "\r\n"
            self.writer.transmit_queue.put(bytes(message, 'utf-8'))
            #print(message)
            #byte_message = bytes(message, 'utf-8')
            # self.communicate.write(byte_message)
            #print(argument)
            # read = str(self.communicate.readline().decode('utf-8'))
            # print(read)
            # sleep(3)
            # self.reader.receive_data()
            # self.reader.print_received_message
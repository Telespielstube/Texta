import gpiozero
from time import sleep

led = LED(18)

while True:   
    gpiozero.led.off()
    sleep(3)
    gpiozero.led.on()
    print('Lora mcu reset successful!')
    exit(0)

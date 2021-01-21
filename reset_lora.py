from gpiozero import LED
from time import sleep

led = LED(18)

while True:   
    led.off()
    sleep(3)
    led.on()
    print('Lora mcu reset successful!')
    exit(0)

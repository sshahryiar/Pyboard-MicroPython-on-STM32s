"""
Notes

1. Thonny or any other IDE cannot run simultaneously when a program like Putty or similar is being used for manipulating COM port

2. Port: Same as the COM ID of the Pyboard

3. Baud Rate: 115200   Parity: None    Stop: 1

4. Must uncomment the following line

pyb.usb_mode('VCP+HID') 

in the boot.py file or else USB function won't work at all 
"""

from pyb import Pin, ADCAll, USB_VCP
from machine import I2C
from time import sleep_ms, sleep_us
from SH1107 import OLED


SW = Pin('A0', Pin.IN, Pin.PULL_UP)
click = Pin('A1', Pin.IN, Pin.PULL_UP)
LED = Pin('C13', Pin.OUT)

adc = ADCAll(12, 0x70000)

TWI = I2C(scl = 'PB9', sda = 'PB8', freq = 100000)
oled = OLED(TWI)

usb = USB_VCP()

oled.fill(oled.BLACK)
oled.show()


buffer = ""
compensation = 0


def get_T_avg(no_of_samples = 120):
    samples = no_of_samples
    tmp = 0
    
    while(samples > 0):
        tmp += adc.read_core_temp()
        sleep_us(20)        
        samples -= 1     
    
    tmp /= no_of_samples
    tmp += compensation
        
    return tmp


usb.setinterrupt(-1)

while (SW.value() == True):
    
    t = get_T_avg()   
    
    if(usb.any()):
        LED.on()
        buffer = usb.readline()
        buffer = buffer[0:(len(buffer) - 2)]
        
        if(buffer[0] == 45):
            compensation = -(((buffer[1] - 48) * 10) + (buffer[2] - 48))
        else:
            compensation = (((buffer[0] - 48) * 10) + (buffer[1] - 48))
            
    usb.write(str("%4.4f" %t) + "\r\n")
    
    oled.fill(oled.BLACK)
    
    oled.text("PyB USB CDC", 15, 1, oled.WHITE)
    oled.text("Comp/'C: ",  1, 20, oled.WHITE)
    oled.text(str("%2d" %compensation), 80, 20, oled.WHITE)
    oled.text("Temp/'C: ",  1, 40, oled.WHITE)
    oled.text(str("%2.2f" %t), 80, 40, oled.WHITE)
    oled.show()
    LED.off()
    sleep_ms(400)
    
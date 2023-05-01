from pyb import LED, Pin
from utime import sleep_ms


i = 0
j = 0
k = 1


led_1 = LED(1)
led_2 = LED(2)
led_3 = LED(3)
led_4 = LED(4)


bt_1 = Pin('X9', Pin.IN, Pin.PULL_NONE)
bt_2 = Pin('X10', Pin.IN, Pin.PULL_NONE)
bt_3 = Pin('X11', Pin.IN, Pin.PULL_NONE)
bt_4 = Pin('X12', Pin.IN, Pin.PULL_NONE)

sleep_ms(10000)


while(True):
    if(bt_1.value() == True):
        sleep_ms(60)
        if(bt_1.value() == True):
            led_1.on()
        else:
            led_1.off()
            
    if(bt_2.value() == True):
        sleep_ms(60)
        if(bt_2.value() == True):
            led_2.toggle()
            sleep_ms(100)
            
    if(bt_3.value() == True):
        sleep_ms(60)
        if(bt_3.value() == True):
            for i in range (0, 255, 10):
                led_3.intensity(i)
                sleep_ms(60)
            for i in range (255, 0, -10):
                led_3.intensity(i)
                sleep_ms(60)            
            led_3.off()
                
    if(bt_4.value() == True):
        sleep_ms(60)
        if(bt_4.value() == True):
            j += k
            if(j >= 255):
                k = -1
            if(j <= 0):
                k = 1
            led_4.intensity(j)
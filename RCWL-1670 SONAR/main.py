from pyb import LED
from machine import I2C
from utime import sleep_ms
from RGB_LCD import RGB_LCD
from SONAR import SONAR


led = LED(3)

i2c = I2C(1, freq = 400000)

lcd = RGB_LCD(i2c)

RCWL1670 = SONAR('X5', 'X4', 15, 5.8)


def measure_and_show():
    led.on()
    distance = RCWL1670.get_range()
    sleep_ms(300)
    
    if((distance >= 0) and (distance < 200)):
        lcd.set_RGB(255, 0, 0)
        
    elif((distance >= 200) and (distance < 400)):
        lcd.set_RGB(255, 255, 0)
        
    elif((distance >= 240) and (distance < 600)):
        lcd.set_RGB(0, 255, 255)
    
    elif((distance >= 600) and (distance < 800)):
        lcd.set_RGB(0, 0, 255)
        
    else:
        lcd.set_RGB(255, 255, 255)
    
    lcd.goto_xy(1, 0)
    lcd.put_str("PYB RCWL SONAR")
    lcd.goto_xy(0, 1)
    lcd.put_str("Range/mm: " + str("%3u  " %distance))

    led.off()
    sleep_ms(300)
    

while(True):   
    measure_and_show()  

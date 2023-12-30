"""
Must uncomment the following line

pyb.usb_mode('VCP+HID') 

in the boot.py file or else USB function won't work at all 

"""


from pyb import Pin, ADCAll, Timer, USB_HID
from machine import I2C
from time import sleep_ms, sleep_us
from SH1107 import OLED


SW = Pin('A0', Pin.IN, Pin.PULL_UP)
click = Pin('A1', Pin.IN, Pin.PULL_UP)
LED = Pin('C13', Pin.OUT)

adc = ADCAll(12, 0x000C)

TWI = I2C(scl = 'PB9', sda = 'PB8', freq = 100000)
oled = OLED(TWI)

hid = USB_HID()


def draw_circle(xc, yc, r, f, colour):
       a = 0
       b = r
       p = (1 - b)
       
       while(a <= b):
           if(f == True):
               oled.line((xc - a), (yc + b), (xc + a), (yc + b), colour)
               oled.line((xc - a), (yc - b), (xc + a), (yc - b), colour)
               oled.line((xc - b), (yc + a), (xc + b), (yc + a), colour)
               oled.line((xc - b), (yc - a), (xc + b), (yc - a), colour)
               
           else:
               oled.pixel((xc + a), (yc + b), colour)
               oled.pixel((xc + b), (yc + a), colour)
               oled.pixel((xc - a), (yc + b), colour)
               oled.pixel((xc - b), (yc + a), colour)
               oled.pixel((xc + b), (yc - a), colour)
               oled.pixel((xc + a), (yc - b), colour)
               oled.pixel((xc - a), (yc - b), colour)
               oled.pixel((xc - b), (yc - a), colour)
            
           if(p < 0):
               p += (3 + (2 * a))
               a += 1
            
           else:
               p += (5 + (2 * (a  - b)))
               a += 1
               b -= 1


def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min) / (x_max - x_min)) * (v - x_min)))


def get_xy_avg(no_of_samples = 64):
    samples = no_of_samples
    x_pos = 0
    y_pos = 0
    
    while(samples > 0):
        x_pos += adc.read_channel(2)
        sleep_us(20)
        
        y_pos += adc.read_channel(3)
        sleep_us(20)
        
        samples -= 1     
    
    x_pos //= no_of_samples    
    y_pos //= no_of_samples
        
    return x_pos, y_pos


oled.fill(oled.BLACK)
oled.show()
sleep_ms(100)
X_comp, Y_comp = get_xy_avg(512)


while(SW.value() == True):
    XV, YV = get_xy_avg()
    
    XV -= X_comp
    YV -= Y_comp
    
    XV = map_value(XV, -2000, 2000, -100, 100)
    YV = map_value(YV, -2000, 2000, -100, 100)
    
    oled.fill(oled.BLACK)
    
    draw_circle(96, 36, 24, False, oled.WHITE)
    
    xp = map_value(XV, -100, 100, -15, 15)
    yp = map_value(YV, -100, 100, -15, 15)
    
    draw_circle((96 + xp), (36 + yp), 2, True, oled.WHITE)
    
    string1 = "X: " + str(XV)
    string2 = "Y: " + str(YV)
    oled.text("Pointer Location", 1, 1, oled.WHITE)
    oled.text(string1, 1, 20, oled.WHITE)
    oled.text(string2, 1, 40, oled.WHITE)
    print(string1 + "   " + string2)
    oled.show()
    
    if(click.value() == False):
        click_state = True
        LED.off()
        
    else:
        click_state = False
        LED.on()
    
    hid.send((click_state, XV, YV, 0))
    sleep_ms(1)

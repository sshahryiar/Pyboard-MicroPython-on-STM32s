from pyb import Pin, SPI, Servo, ADC
from SSD1309 import OLED1309
from utime import sleep_ms, sleep_us
from micropython import const
from math import cos, sin


step_size = const(1)
min_angle = const(0)
max_angle = const(60)
min_range = const(0)
max_range = const(1200)


i = min_angle
j = step_size
l = 0
r = 0
r_min = max_range
r_max = min_range
x_pos = 0
y_pos = 0
deg_to_rad = 0.017456
direction_change = True


cs_pin = Pin('PB7', Pin.OUT_PP)
dc_pin = Pin('PB8', Pin.OUT_PP)
rst_pin = Pin('PB9', Pin.OUT_PP)

sonar = ADC(Pin("PA1"))

spi = SPI(2, mode = SPI.MASTER, baudrate = 4000000, polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB)

oled = OLED1309(spi, dc_pin, rst_pin, cs_pin)

servo = Servo(1)


def map_value(value, x_min, x_max, y_min, y_max):
    return (y_min + (((y_max - y_min) / (x_max - x_min)) * (value - x_min)))


def constrain(value, min_value, max_value):
    if(value > max_value):
        return max_value
    
    elif(value < min_value):
        return min_value
    
    else:
        return value


def circle(xc, yc, r, c):
   a = 0
   b = r
   p = (1 - b)
   
   while(a <= b):
       oled.pixel((xc + a), (yc + b), c)
       oled.pixel((xc + b), (yc + a), c)
       oled.pixel((xc - a), (yc + b), c)
       oled.pixel((xc - b), (yc + a), c)
       oled.pixel((xc + b), (yc - a), c)
       oled.pixel((xc + a), (yc - b), c)
       oled.pixel((xc - a), (yc - b), c)
       oled.pixel((xc - b), (yc - a), c)
        
       if(p < 0):
           p += (3 + (2 * a))
           a += 1
        
       else:
           p += (5 + (2 * (a  - b)))
           a += 1
           b -= 1  


oled.fill(oled.BLACK)
oled.show()


while(True):
    if(direction_change):
        oled.fill(oled.BLACK)
    
        for k in range (0, 7):
            circle(63, 63, (10 * k), oled.WHITE)
        
        r_min /= 1000.0
        r_max /= 1000.0
        
        oled.text(str("%1.1f" %r_min), 1, 1, oled.WHITE)
        oled.text(str("%1.1f" %r_max), 100, 1, oled.WHITE)
        
        oled.text("m", 10, 10, oled.WHITE)
        oled.text("m", 110, 10, oled.WHITE)
        
        
        r_min = max_range
        r_max = min_range        
        direction_change = False
        
    servo.angle(i)
    sleep_ms(100)
    
    r = (sonar.read() / 3)
    r = constrain(r, min_range, max_range)
    
    if(r < r_min):
        r_min = r
        
    if(r > r_max):
        r_max = r
    
    l = map_value(r, min_range, max_range, 0, 60)

    x_pos = int(63 + (l * (cos(deg_to_rad * (i * 3)))))
    y_pos = int(63 - (l * (sin(deg_to_rad * (i * 3)))))
    
    oled.line(63, 63, x_pos, y_pos, oled.WHITE)
    
    print("Angle: " + str("%02u" %i) + "   Range/mm: " + str("%03.1f" %r))
    
    i += j
    
    if(i == max_angle):
        j = -(step_size)
        direction_change = True
        
    if(i == min_angle):
        j = step_size
        direction_change = True
    
    oled.show()
        
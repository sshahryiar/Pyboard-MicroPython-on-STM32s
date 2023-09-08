from pyb import Pin, SPI, Timer
from SSD1309 import OLED1309
from utime import sleep_ms, sleep_us
from micropython import const


points = const(32)


f = 1
i = 0
j = 0
k = 0
pulse = 1
last_capture = 0
bar = bytearray(b'\x3F' * points)


cs_pin = Pin('PB7', Pin.OUT_PP) #'PB7'
dc_pin = Pin('PB8', Pin.OUT_PP) #'PB8'
rst_pin = Pin('PB9', Pin.OUT_PP) #'PB9'
cap_pin = Pin('PA1', Pin.IN)

spi = SPI(2, mode = SPI.MASTER, baudrate = 1000000, polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB)

oled = OLED1309(spi, dc_pin, rst_pin, cs_pin)


def input_capture(timer):
    global last_capture, pulse
    
    pulse = (in_cap.capture() - last_capture)
    last_capture = in_cap.capture()
    pulse &= 0x0FFFFFFF


TIM2 = Timer(2,
             prescaler = 10,
             period = 0x0FFFFFFF)

in_cap = TIM2.channel(2,
                      mode = Timer.IC,
                      pin = cap_pin,
                      polarity = Timer.RISING,
                      callback = input_capture)


def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min) / (x_max - x_min)) * (v - x_min)))


def constrain(value, min_value, max_value):
    if(value > max_value):
        return max_value
    
    elif(value < min_value):
        return min_value
    
    else:
        return value


oled.fill(oled.BLACK)
oled.show()


while(True):
    f = (4000 / pulse)
    f = constrain(f, 1, 100)
    
    bar[j] = map_value(f, 1, 100, 63, 25)
    
    oled.fill(oled.BLACK)
    oled.text("PYB TSL235", 20, 4, oled.WHITE)
    oled.text(("F./kHz: " + str("%3.1f " %f)), 15, 15, oled.WHITE)
    
    for k in range (0, points, 1):
        oled.fill_rect((k * 4), bar[k], 2, (63 - bar[k]), oled.WHITE)
    
    j += 1
    
    if(j >= points):
        j = 0
    
    oled.show()
    sleep_ms(100)

from pyb import LED, UART
from utime import sleep_ms, sleep_us
from PCD8544 import PCD8544
from WS_ToF import waveshare_ToF


distance = 0
strength = 0


led = LED(4)

uart = UART(6, 115200, bits = 8, parity = None, stop = 1, timeout = 1000, rxbuf = 32)

tof = waveshare_ToF(uart)
tof.settings(baud_rate = 115200)

glcd = PCD8544()

glcd.fill(glcd.WHITE)
glcd.show()


def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min) / (x_max - x_min)) * (v - x_min)))


def constrain(value, min_value, max_value):
    if(value > max_value):
        return max_value
    
    elif(value < min_value):
        return min_value
    
    else:
        return value
    
    
def get_distance():
    global distance, strength
    
    tof.inquire_sensor(0, delay = 10)
    ID, time, distance, status, strength, precision = tof.read_sensor(delay = 10)


def display():
    global distance, strength
    
    bar = map_value(distance, 0, 5000, 2, 80)
    bar = constrain(bar, 0, 5000)
    
    glcd.fill(glcd.WHITE)
    glcd.text("ToF LASER", 4 , 2, glcd.BLACK)
    glcd.text("D/mm: " + str("%3u  " %distance), 1 , 16, glcd.BLACK)
    glcd.text("Strn: " + str("%3u  " %strength), 1 , 26, glcd.BLACK)
    
    for i in range(0, bar, 4):
        glcd.vline(i, 37, 8, glcd.BLACK)
        glcd.vline((i - 2), 39, 4, glcd.BLACK)   
    
    glcd.show()
    led.toggle()
    

while(True):
    get_distance()
    display()
    sleep_ms(100)

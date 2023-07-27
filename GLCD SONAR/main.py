from pyb import Pin, LED, Timer
from utime import sleep_ms, sleep_us
from PCD8544 import PCD8544


last_capture = 0
pulse_width = 0


led = LED(1)

echo_pin = Pin('X4', Pin.IN)
trigger_pin = Pin('X5', Pin.OUT_PP)


glcd = PCD8544()

glcd.fill(glcd.WHITE)
glcd.show()


def input_capture(timer):
    global last_capture, pulse_width
    
    if echo_pin.value(): 
        last_capture = in_cap.capture()
        
    else: 
        pulse_width = (in_cap.capture() - last_capture)
        pulse_width &= 0x0FFFFFFF


TIM2 = Timer(2,
             prescaler = 83,
             period = 0x0FFFFFFF)

in_cap = TIM2.channel(4,
                      mode = Timer.IC,
                      pin = echo_pin,
                      polarity = Timer.BOTH,
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


def trigger_sensor():
    led.on()
    trigger_pin.high()
    sleep_us(20)
    trigger_pin.low()
    sleep_ms(300)


def display():
    global pulse_width
        
    distance = constrain(pulse_width, 0, 42000)
    distance = (pulse_width / 5.8)
    bar = map_value(distance, 0, 4000, 2, 80)
    
    glcd.fill(glcd.WHITE)
    glcd.text("PYB SONAR", 4 , 2, glcd.BLACK)
    glcd.text("D/mm: " + str("%3u  " %distance), 1 , 16, glcd.BLACK)
    
    for i in range(2, 83, 10):
        glcd.vline(i, 42, 5, glcd.BLACK)
        glcd.vline((i - 5) , 42, 3, glcd.BLACK)   
    
    glcd.rect(1, 32, 83, 8, glcd.BLACK)
    glcd.rect(2, 34, bar, 4, glcd.BLACK, True)
    
    glcd.show()
    pulse_width = 0
    led.off()
    sleep_ms(300)
    

while(True):
    trigger_sensor()    
    display()  

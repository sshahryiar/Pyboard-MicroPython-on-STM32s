from pyb import LED, Pin, Timer
from machine import I2C
from micropython import const
from SSD1306_I2C import OLED1306
from utime import sleep_ms


STEPS = const(1000)

count = 0
step_size = 1
past_value = 1


led = LED(1)


TWI = I2C(scl = 'PB9', sda = 'PB8', freq = 400000)


oled = OLED1306(TWI)
oled.fill(oled.BLACK)
oled.show()


args = {'pull': Pin.PULL_UP, 'af': Pin.AF2_TIM5}
enc_a_pin = Pin('PA0', mode = Pin.AF_OD, **args)
enc_b_pin = Pin('PA1', mode = Pin.AF_OD, **args)


timer = Timer(5, prescaler = 2, period = ((STEPS << 1) - 1))
channel = timer.channel(1, Timer.ENC_AB)
timer.counter(0)


def write_text(text, x, y, size, color):
        background = oled.pixel(x, y)
        info = []
        
        oled.text(text, x, y, color)
        for i in range(x, x + (8 * len(text))):
            for j in range(y, y + 8):
                px_color = oled.pixel(i, j)
                info.append((i, j, px_color)) if px_color == color else None
        
        oled.text(text, x, y, background)
       
        for px_info in info:
            oled.fill_rect(size*px_info[0] - (size-1) * x , size * px_info[1] - (size-1) * y, size, size, px_info[2]) 


while(True):
    count = (timer.counter() >> 1) 
    
    if(past_value != count):
        led.on()
        oled.fill(oled.BLACK)
        oled.text("Rotary Encoder", 8, 2, oled.WHITE)
        write_text(str("%03u" %count), 15, 20, 4, oled.WHITE)
        oled.show()
        past_value = count
        sleep_ms(100)
        led.off()
        sleep_ms(100)
    
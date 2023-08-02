from pyb import LED, Pin, ExtInt
from machine import I2C
from micropython import const
from SSD1306_I2C import OLED1306
from utime import sleep_ms


MAX_count = const(1000)
MIN_count = const(-1000)

count = 0
step_size = 1
past_value = 1


led = LED(1)


TWI = I2C(scl = 'PB9', sda = 'PB8', freq = 400000)


oled = OLED1306(TWI)
oled.fill(oled.BLACK)
oled.show()


sw_pin = Pin('PA0', Pin.IN, Pin.PULL_UP)
enc_a_pin = Pin('PA2', Pin.IN, Pin.PULL_NONE) 
enc_b_pin = Pin('PA3', Pin.IN, Pin.PULL_NONE)


def EXTI_ENC_A(pin): 
    global count
    
    state_of_A = enc_a_pin.value()
    state_of_B = enc_b_pin.value()
    
    if((state_of_A == True) and (state_of_B == False)):
        count -= step_size

    if(count > MAX_count):
        count = MIN_count   
    

def EXTI_ENC_B(pin):
    global count
    
    state_of_A = enc_a_pin.value()
    state_of_B = enc_b_pin.value()
           
    if((state_of_A == False) and (state_of_B == True)):
        count += step_size
    
    if(count < MIN_count):
        count = MAX_count
        
        
EXTI_A = ExtInt(enc_a_pin,
                ExtInt.IRQ_RISING,
                Pin.PULL_NONE,
                EXTI_ENC_A)   

EXTI_B = ExtInt(enc_b_pin,
                ExtInt.IRQ_RISING,
                Pin.PULL_NONE,
                EXTI_ENC_B)


while(True):
    if(sw_pin.value() == False):
        led.on()
        sleep_ms(400)
        led.off()
        while(sw_pin.value() == False):
            pass
        step_size *= 10
        
        if(step_size > 1000):
            step_size = 1
    
    if(past_value != count):
        led.on()
        oled.fill(oled.BLACK)
        oled.text("AEDR8300 Encoder", 1, 2, oled.WHITE)
        oled.text("Value: " + str("%03u" %count), 1, 20, oled.WHITE)
        oled.show()
        past_value = count
        sleep_ms(100)
        led.off()
        sleep_ms(100)
    
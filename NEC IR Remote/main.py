from micropython import *
from pyb import *
from machine import I2C, Pin
from utime import sleep_ms
from I2C_LCD import TWI_LCD
import gc


HIGH_Max = const(2000)
HIGH_Min = const(1300)

LOW_Max = const(700)
LOW_Min = const(400)


ir_code = 0
bit_count = 0


led1 = LED(1)
led2 = LED(2)
led3 = LED(3)
led4 = LED(4)

IR_Pin = Pin("X1", Pin.IN, Pin.PULL_UP)

i2c = I2C(1, freq = 400000)

lcd = TWI_LCD(i2c)


lcd.text("PYB NEC Decoder", 0, 0)
lcd.text("IR Data:", 0, 1)


def capture_pulses(timer):
    global bit_count, ir_code
    
    disable_irq()
    
    if(IR_Pin.value()):
        TIM.counter(0)
        pulse_width = 0
        
    else:
        pulse_width = TIM_IC.capture()
        print(pulse_width)
        
        if((pulse_width >= LOW_Min) and (pulse_width <= HIGH_Max)):
            ir_code <<= 1
        
        if(pulse_width >= HIGH_Min):
            if(pulse_width <= HIGH_Max):
                ir_code |= 1
        
        elif(pulse_width <= LOW_Max):
            if(pulse_width >= LOW_Min):
                ir_code |= 0
    
        bit_count += 1
        
    enable_irq()
             
        
TIM = Timer(2, prescaler = 83, period = 65535)

print(TIM.freq())
print(TIM.period())
print(TIM.prescaler())

TIM_IC = TIM.channel(1,
                     mode = Timer.IC,
                     pin = IR_Pin,
                     polarity = Timer.BOTH,
                     callback = capture_pulses)


while(True):
    if(bit_count >= 34):
        text = "0x" + str("%X" %ir_code)
        print("IR Code: " + text)
        lcd.text(text, 8, 1)
        
        if(ir_code == 0xFF30CF):
            led1.toggle()
            
        elif(ir_code == 0xFF18E7):
            led2.toggle()
            
        elif(ir_code == 0xFF7A85):
            led3.toggle()
            
        elif(ir_code == 0xFF10EF):
            led4.toggle()
        
        elif(ir_code == 0xFF38C7):
            led1.on()
            led2.on()
            led3.on()
            led4.on()
        
        else:
            led1.off()
            led2.off()
            led3.off()
            led4.off()
        
        ir_code = 0
        bit_count = 0
        gc.collect()
        alloc_emergency_exception_buf(100)
        sleep_ms(400)

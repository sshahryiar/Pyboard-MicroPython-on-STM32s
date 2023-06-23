from pyb import Timer, ADC, Pin
from seven_segment_display import seg_disp
from utime import sleep_ms, sleep_us


seg = 0
value = 0


adc_pin = Pin('X1', Pin.ANALOG)
adc = ADC(adc_pin)


def get_T():
    samples = 64
    temp = 0
    
    while(samples > 0):
        temp += adc.read()
        sleep_us(20)
        samples -= 1
    
    temp >>= 6
    
    return int(temp // 1.5)


def timer_tick(t):
    global seg, value
    
    val = 0
    point = False
    
    if(seg == 3):
        val = (value // 100)
    elif(seg == 2):
        val = ((value % 100) // 10)
        point = True
    elif(seg == 1):
        val = (value % 10)
    else:
        val = 12
    
    disp.write(val, seg, point)
    
    seg += 1
   
    if(seg > 3):
        seg = 0
    

tim = Timer(2, freq = 400, callback = timer_tick)
disp = seg_disp()


while True:
    value = get_T()
    sleep_ms(600)  
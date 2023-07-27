from pyb import Pin, Timer
from utime import sleep_us, sleep_ms


class SONAR():
    
    def __init__(self, _trigger = 'X5', _echo = 'X4', _pulse_time = 15, _scaling_factor = 5.8):
        self.last_capture = 0
        self.pulse_width = 0
        self.pulse_time = _pulse_time
        self.scaling_factor = _scaling_factor
        self.echo = Pin(_echo, Pin.IN)
        self.trigger = Pin(_trigger, Pin.OUT_PP)
        self.init()
        
        
    def input_capture(self, timer):        
        if(self.echo.value()): 
            self.last_capture = self.in_cap.capture()
            
        else: 
            self.pulse_width = (self.in_cap.capture() - self.last_capture)
            self.pulse_width &= 0x0FFFFFFF
                
        
    def init(self):
        self.trigger.low()
        
        self.TIM2 = Timer(2,
                          prescaler = 83,
                          period = 0x0FFFFFFF)

        self.in_cap = self.TIM2.channel(4,
                                        mode = Timer.IC,
                                        pin = self.echo,
                                        polarity = Timer.BOTH,
                                        callback = self.input_capture)


    def trigger_sensor(self):
        self.trigger.high()
        sleep_us(self.pulse_time)
        self.trigger.low()
   
        
    def get_range(self):        
        self.trigger_sensor()
        sleep_ms(200)        
        distance = (self.pulse_width / self.scaling_factor)
        self.pulse_width = 0
        
        return distance
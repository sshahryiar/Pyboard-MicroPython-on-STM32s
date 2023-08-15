from micropython import const
from utime import sleep_us


one = const(0xF8)
zero = const(0xC0)

number_of_colour_channels = const(3)
number_of_bits_per_channel = const(8)
number_of_bits = (number_of_colour_channels * number_of_bits_per_channel)


class WS2812():
    
    def __init__(self, _no_of_LEDs, _spi):
        self.no_of_LEDs = _no_of_LEDs
        self.spi = _spi
        
        self.buffer_size = (self.no_of_LEDs * number_of_bits)
        self.buffer = bytearray(self.buffer_size)
        
        self.reset()
        
        
    def reset(self):
        for i in range(0, self.buffer_size):
            self.buffer[i] = 0x00
            
        self.set_all_channel(0, 0, 0)
        
        
    def send(self, channel, r, g, b):
        s = 0
        n = (number_of_bits * channel)
        temp = 0
        value = 0x00000000
        value = ((g << 16) | (r << 8) | b)
        
        while(s < number_of_bits):
            if(value & 0x800000):
                temp = one
            
            else:
                temp = zero
                
            self.buffer[s + n] = temp
            value <<= 1
            s += 1       
             
        
    def set_all_channel(self, r, g, b):
        for i in range(0, self.no_of_LEDs):
            self.send(i, r, g, b)     
        self.show()
        
        
    def show(self):
        self.spi.send(self.buffer)
        sleep_us(60)
            
    
        
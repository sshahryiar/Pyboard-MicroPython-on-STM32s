from micropython import const
from pyb import Pin
from onewire import OneWire
from utime import sleep_ms


convert_T = const(0x44)
read_scratchpad = const(0xBE)            
write_scratchpad = const(0x4E) 
copy_scratchpad = const(0x48)   
recall_E2 = const(0xB8) 
read_power_supply = const(0xB4)    
skip_ROM = const(0xCC)


class DS18B20():
    
    def __init__(self, _pin):
        self.pin = Pin(_pin, Pin.IN, Pin.PULL_UP)
        self.ow = OneWire(self.pin)
        
        self.init()
        
    
    def init(self):
        self.ow.reset()        
        sleep_ms(400)
        
        
    def get_T(self):
        msb = 0
        lsb = 0
        temp = 0.0
        
        self.ow.reset()
        self.ow.writebyte(skip_ROM)
        self.ow.writebyte(convert_T)
        sleep_ms(800)
        
        self.ow.reset()
        self.ow.writebyte(skip_ROM)
        self.ow.writebyte(read_scratchpad)
        
        lsb = self.ow.readbyte()
        msb = self.ow.readbyte()

        temp = msb                         
        temp <<= 8 
        temp |= lsb
        temp *= 0.0625
        
        return temp
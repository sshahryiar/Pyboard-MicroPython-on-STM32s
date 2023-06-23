from pyb import Pin


mosi_pin = 'Y8'
sck_pin = 'Y6'
rclk_pin = 'Y5'


seg_code_list = [
    0xC0, # 0
    0xF9, # 1
    0xA4, # 2
    0xB0, # 3
    0x99, # 4
    0x92, # 5
    0x82, # 6
    0xF8, # 7
    0x80, # 8
    0x90, # 9
    0x88, # A
    0x83, # b
    0xC6, # C
    0xA1, # d
    0x86, # E
    0x8E, # F
]

seg_pos_list = [
    0x01, # 1st
    0x02, # 2nd
    0x04, # 3rd
    0x08, # 4th  
]


class seg_disp():
    
    def __init__(self):
        self.mosi = Pin(mosi_pin, Pin.OUT_PP)
        self.sck = Pin(sck_pin, Pin.OUT_PP)
        self.rclk = Pin(rclk_pin, Pin.OUT_PP)


    def write(self, value, pos, dot):
        temp = seg_code_list[value]
        if(dot == True):
            temp &= 0x7F
            
        self.rclk.low()        
        self.write_register(temp)
        self.write_register(seg_pos_list[pos])
        self.rclk.high()
        
    
    def write_register(self, value):
        clks = 8
        
        while(clks > 0):
            if((value & 0x80) != 0x00):
                self.mosi.high()
            else:
                self.mosi.low()

            self.sck.high()            
            value <<= 1
            clks -= 1
            self.sck.low()
from micropython import const
from pyb import Pin, SPI
from utime import sleep_ms
from ustruct import pack
import framebuf


PCD8544_DC_pin = 'X2'
PCD8544_CS_pin = 'X3'
PCD8544_RST_pin = 'X1'
PCD8544_SCK_pin = 'X6'
PCD8544_MOSI_pin = 'X8'

PCD8544_FUNCTION_SET     = const(0x20)
PCD8544_POWER_DOWN       = const(0x04)
PCD8544_ADDRESSING_VERT  = const(0x02)
PCD8544_EXTENDED_INSTR   = const(0x01)

PCD8544_DISPLAY_BLANK    = const(0x08)
PCD8544_DISPLAY_ALL      = const(0x09)
PCD8544_DISPLAY_NORMAL   = const(0x0C)
PCD8544_DISPLAY_INVERSE  = const(0x0D)

PCD8544_TEMP_COEFF_0     = const(0x04)
PCD8544_TEMP_COEFF_1     = const(0x05)
PCD8544_TEMP_COEFF_2     = const(0x06) 
PCD8544_TEMP_COEFF_3     = const(0x07)

PCD8544_BIAS_1_100       = const(0x10)
PCD8544_BIAS_1_80        = const(0x11)
PCD8544_BIAS_1_65        = const(0x12)
PCD8544_BIAS_1_48        = const(0x13)
PCD8544_BIAS_1_40        = const(0x14) 
PCD8544_BIAS_1_24        = const(0x15)
PCD8544_BIAS_1_18        = const(0x16)
PCD8544_BIAS_1_10        = const(0x17)
PCD8544_SET_VOP          = const(0x80)
PCD8544_COL_ADDR         = const(0x80)
PCD8544_BANK_ADDR        = const(0x40) 

CMD = False
DAT = True

LOW = False
HIGH = True

PCD8544_GLCD_WIDTH = const(84)
PCD8544_GLCD_HEIGHT = const(48)


class PCD8544(framebuf.FrameBuffer):
    def __init__(self):
        self.width = PCD8544_GLCD_WIDTH
        self.height = PCD8544_GLCD_HEIGHT
        
        self.BLACK = const(0xFF)
        self.WHITE = const(0x00)

        self.PCD8544_CS = Pin(PCD8544_CS_pin, Pin.OUT_PP)
        self.PCD8544_RST = Pin(PCD8544_RST_pin, Pin.OUT_PP)
        self.PCD8544_SCK = Pin(PCD8544_SCK_pin, Pin.OUT_PP)
        self.PCD8544_MOSI = Pin(PCD8544_MOSI_pin, Pin.OUT_PP)

        self.PCD8544_SPI = SPI(1, SPI.CONTROLLER, baudrate = 4_000_000, polarity = 0, phase = 0)
        
        self.PCD8544_DC = Pin(PCD8544_DC_pin, Pin.OUT_PP)
        
        self.buffer = bytearray((self.height * self.width) // 8) #84 x 48 = 504
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        
        self.init()



    def init(self):
        self.function = PCD8544_FUNCTION_SET
        self.disp_reset()
        self.addressing(True)
        self.set_contrast(PCD8544_BIAS_1_40, PCD8544_TEMP_COEFF_2, 63)
        self.disp_invert(False)
        self.clear()


    def disp_reset(self):
        self.PCD8544_CS.value(HIGH)
        self.PCD8544_DC.value(HIGH)

        self.PCD8544_RST.value(HIGH)
        sleep_ms(10)
        self.PCD8544_RST.value(LOW)
        sleep_ms(20)
        self.PCD8544_RST.value(HIGH)


    def send(self, value, mode):
        self.PCD8544_CS.value(LOW)
        self.PCD8544_DC.value(mode)
        
        if(mode == DAT):
            self.PCD8544_SPI.write(pack('B'*len(value), *value))
        else:
            self.PCD8544_SPI.write(bytearray([value]))
            
        self.PCD8544_CS.value(HIGH)


    def set_xy(self, x_pos, y_pos):
    	self.send((PCD8544_COL_ADDR | x_pos), CMD)
    	self.send((PCD8544_BANK_ADDR | y_pos), CMD)


    def addressing(self, horizontal_or_vertical = True):
    	if(horizontal_or_vertical == True):
    		self.function &= ~PCD8544_ADDRESSING_VERT
    	else:
    		self.function |= PCD8544_ADDRESSING_VERT

    	self.send(self.function, CMD)


    def clear(self):
        self.send(([0] * 504), DAT) #84 x 48 = 504
        self.set_xy(0, 0)


    def disp_invert(self, mode):
        if(mode == True):
            self.send(PCD8544_DISPLAY_INVERSE, CMD)
        else:
            self.send(PCD8544_DISPLAY_NORMAL, CMD)


    def disp_power(self, mode):
        if(mode == True):
            self.function &= ~PCD8544_POWER_DOWN
        else:
            self.function |= PCD8544_POWER_DOWN

        self.send(self.function, CMD)


    def set_contrast(self, bias = PCD8544_BIAS_1_40, t_coff = PCD8544_TEMP_COEFF_2, contrast = 63):
        self.send((self.function | PCD8544_EXTENDED_INSTR), CMD)
        self.send(t_coff, CMD)
        self.send(bias, CMD)
        self.send(PCD8544_SET_VOP | contrast, CMD)
        self.send((self.function & ~PCD8544_EXTENDED_INSTR), CMD)
        
        
        
    def show(self):
    	self.send(self.buffer, DAT)


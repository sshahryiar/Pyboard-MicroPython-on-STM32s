from micropython import const
from machine import Pin
from utime import sleep_ms
import framebuf  


disp_width                                   = const(128)
disp_height                                  = const(64)
disp_pages                                   = const((disp_height >> 3))

# Constants
SSD1309_SET_CONTRAST                         = const(0x81)
SSD1309_DISPLAY_ALL_ON_RESUME                = const(0xA4)
SSD1309_DISPLAY_ALL_ON                       = const(0xA5)
SSD1309_NORMAL_DISPLAY                       = const(0xA6)
SSD1309_INVERT_DISPLAY                       = const(0xA7)
SSD1309_DISPLAY_OFF                          = const(0xAE)
SSD1309_DISPLAY_ON                           = const(0xAF)
SSD1309_SET_DISPLAY_OFFSET                   = const(0xD3)
SSD1309_SET_COM_PINS                         = const(0xDA)
SSD1309_SET_VCOM_DETECT                      = const(0xDB)
SSD1309_SET_DISPLAY_CLOCK_DIV                = const(0xD5)
SSD1309_SET_PRECHARGE                        = const(0xD9)
SSD1309_SET_MULTIPLEX                        = const(0xA8)
SSD1309_SET_LOW_COLUMN                       = const(0x00)
SSD1309_SET_HIGH_COLUMN                      = const(0x10)
SSD1309_SET_START_LINE                       = const(0x40)
SSD1309_MEMORY_MODE                          = const(0x20)
SSD1309_COLUMN_ADDR                          = const(0x21)
SSD1309_PAGE_ADDR                            = const(0x22)
SSD1309_COM_SCAN_INC                         = const(0xC0)
SSD1309_COM_SCAN_DEC                         = const(0xC8)
SSD1309_SEG_REMAP                            = const(0xA0)
SSD1309_CHARGE_PUMP                          = const(0x8D)
SSD1309_EXTERNAL_VCC                         = const(0x01)
SSD1309_SWITCH_CAP_VCC                       = const(0x02)

# Scrolling constants
SSD1309_ACTIVATE_SCROLL                      = const(0x2F)
SSD1309_DEACTIVATE_SCROLL                    = const(0x2E)
SSD1309_SET_VERTICAL_SCROLL_AREA             = const(0xA3)
SSD1309_RIGHT_HORIZONTAL_SCROLL              = const(0x26)
SSD1309_LEFT_HORIZONTAL_SCROLL               = const(0x27)
SSD1309_VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = const(0x29)
SSD1309_VERTICAL_AND_LEFT_HORIZONTAL_SCROLL  = const(0x2A)

LOW                                          = const(0)
HIGH                                         = const(1)

CMD = LOW
DAT = HIGH


class OLED1309(framebuf.FrameBuffer):

    def __init__(self, _spi, _dc, _rst, _cs):
        self.width = disp_width
        self.height = disp_height
        self._pages = disp_pages
        
        self.WHITE =   1
        self.BLACK =   0
        
        self.spi = _spi
        self.cs = Pin(_cs, Pin.OUT)
        self.rst = Pin(_rst, Pin.OUT)
        self.dc = Pin(_dc, Pin.OUT)    
        
        self.buffer = bytearray(self._pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()


    def write_command(self, value):
        self.dc.value(CMD)
        self.cs.value(LOW)
        self.spi.write(bytearray([value]))
        self.cs.value(HIGH)


    def reset(self):
        self.rst.value(HIGH)
        sleep_ms(1)
        self.rst.value(LOW)
        sleep_ms(10)
        self.rst.value(HIGH)


    def init_display(self):
        self.reset()

        self.write_command(SSD1309_DISPLAY_OFF)
        self.write_command(SSD1309_SET_DISPLAY_CLOCK_DIV)
        self.write_command(0x80)

        self.write_command(SSD1309_SET_MULTIPLEX)
        self.write_command((self.height - 1))

        self.write_command(SSD1309_SET_DISPLAY_OFFSET)
        self.write_command(0x00)

        self.write_command((SSD1309_SET_START_LINE | 0x00))
   
        self.write_command(SSD1309_CHARGE_PUMP)
        self.write_command(0x14)  # 0x10  # 0x14

        self.write_command(SSD1309_MEMORY_MODE)
        self.write_command(0x00)

        self.write_command((SSD1309_SEG_REMAP | 0x01))
        self.write_command(SSD1309_COM_SCAN_DEC)
        self.write_command(SSD1309_SET_COM_PINS)
        self.write_command(0x12)

        self.write_command(SSD1309_SET_CONTRAST)
        self.write_command(0xCF) # 0x9F # 0xCF

        self.write_command(SSD1309_SET_PRECHARGE)
        self.write_command(0xF1) # 0x22 # 0xF1

        self.write_command(SSD1309_SET_VCOM_DETECT)
        self.write_command(0x40)

        self.write_command(SSD1309_DISPLAY_ALL_ON_RESUME)
        self.write_command(SSD1309_NORMAL_DISPLAY)
        self.write_command(SSD1309_DISPLAY_ON)


    def show(self):
        x0 = 0
        x1 = self.width - 1
        if (self.width == 64):
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
            
        self.write_command(SSD1309_COLUMN_ADDR)
        self.write_command(x0)
        self.write_command(x1)
        self.write_command(SSD1309_PAGE_ADDR)
        self.write_command(0x00)
        self.write_command((self._pages - 1))
        
        self.dc.value(DAT)
        self.cs.value(LOW)
        self.spi.write(self.buffer)
        self.cs.value(HIGH)

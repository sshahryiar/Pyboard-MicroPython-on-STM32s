from micropython import const
from utime import sleep_ms


AiP31068_LCD_I2C_address = const(0x3E)
PCA9633_I2C_address = const(0x60)

REG_RED = const(0x04)
REG_GREEN = const(0x03)
REG_BLUE = const(0x02)
REG_MODE_1 = const(0x00)
REG_MODE_2 = const(0x01)
REG_OUTPUT = const(0x08)

LCD_CLEAR_DISPLAY = const(0x01)
LCD_RETURN_HOME = const(0x02)
LCD_ENTRY_MODE_SET = const(0x04)
LCD_DISPLAY_CONTROL = const(0x08)
LCD_CURSOR_SHIFT = const(0x10)
LCD_FUNCTION_SET = const(0x20)
LCD_SET_CGRAM_ADDR = const(0x40)
LCD_SET_DDRAM_ADDR = const(0x80)

LCD_ENTRY_RIGHT = const(0x00)
LCD_ENTRY_LEFT = const(0x02)
LCD_ENTRY_SHIFT_INCREMENT = const(0x01)
LCD_ENTRY_SHIFT_DECREMENT = const(0x00)

LCD_DISPLAY_ON = const(0x04)
LCD_DISPLAY_OFF = const(0x00)
LCD_CURSOR_ON = const(0x02)
LCD_CURSOR_OFF = const(0x00)
LCD_BLINK_ON = const(0x01)
LCD_BLINK_OFF = const(0x00)

LCD_DISPLAY_MOVE = const(0x08)
LCD_CURSOR_MOVE = const(0x00)
LCD_MOVE_RIGHT = const(0x04)
LCD_MOVE_LEFT = const(0x00)

LCD_8_BIT_MODE = const(0x10)
LCD_4_BIT_MODE = const(0x00)
LCD_2_LINE = const(0x08)
LCD_1_LINE = const(0x00)
LCD_5x8_DOTS = const(0x00)

DAT = const(0x40)
CMD = const(0x80)


class RGB_LCD():
    
    def __init__(self, _i2c):
        self._row = 2
        self._col = 16
        self.i2c = _i2c
        self._showfunction = (LCD_4_BIT_MODE | LCD_1_LINE | LCD_5x8_DOTS)
        self.init(self._row, self._col)
        
        
    def write_to_LCD(self, value, loc):
        self.i2c.writeto_mem(AiP31068_LCD_I2C_address, loc, chr(value))
    
    
    def write_to_RGB_LED(self, reg, value):
        self.i2c.writeto_mem(PCA9633_I2C_address, reg, chr(value))
        
       
    def set_RGB(self, r, g, b):
        self.write_to_RGB_LED(REG_RED, r)
        self.write_to_RGB_LED(REG_GREEN, g)
        self.write_to_RGB_LED(REG_BLUE, b)
        
        
    def goto_xy(self, x_pos, y_pos):
        if(y_pos == 0):
          x_pos |= 0x80
        else:
          x_pos |= 0xC0

        self.i2c.writeto(AiP31068_LCD_I2C_address, bytearray([0x80, x_pos]))
      
      
    def clear_home(self):
        self.write_to_LCD(LCD_CLEAR_DISPLAY, CMD)
        self.write_to_LCD(LCD_RETURN_HOME, CMD)
        sleep_ms(2)
      
      
    def display(self):
        self._showcontrol |= LCD_DISPLAY_ON 
        self.write_to_LCD((LCD_DISPLAY_CONTROL | self._showcontrol), CMD)
    

    def put_chr(self, ch):
        self.write_to_LCD(ord(ch), DAT)
        
        
    def put_str(self, ch_str):
        for chr in ch_str:
            self.put_chr(chr)


    def init(self, cols, rows):
        if (rows > 1):
            self._showfunction |= LCD_2_LINE 
        sleep_ms(50)
        self.write_to_LCD((LCD_FUNCTION_SET | self._showfunction), CMD)
        sleep_ms(5)
        self.write_to_LCD((LCD_FUNCTION_SET | self._showfunction), CMD)
        sleep_ms(5)
        self.write_to_LCD((LCD_FUNCTION_SET | self._showfunction), CMD)
        self.write_to_LCD((LCD_FUNCTION_SET | self._showfunction), CMD)
        self._showcontrol = (LCD_DISPLAY_ON | LCD_CURSOR_OFF | LCD_BLINK_OFF)
        self.display()
        self.clear_home()
        self._showmode = (LCD_ENTRY_LEFT | LCD_ENTRY_SHIFT_DECREMENT)
        self.write_to_LCD((LCD_ENTRY_MODE_SET | self._showmode), CMD)

        self.write_to_RGB_LED(REG_MODE_1, 0x00)
        self.write_to_RGB_LED(REG_OUTPUT, 0xFF)
        self.write_to_RGB_LED(REG_MODE_2, 0x20)
        self.set_RGB(255, 255, 255)

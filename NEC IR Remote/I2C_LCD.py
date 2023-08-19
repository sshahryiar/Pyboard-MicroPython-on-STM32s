from micropython import const
from utime import sleep_ms


default_I2C_address  = const(0x27)

clear_display        = const(0x01)
goto_home            = const(0x02)
         
cursor_direction_inc = const(0x06)
cursor_direction_dec = const(0x04)
display_shift        = const(0x05)
display_no_shift     = const(0x04)

display_on           = const(0x0C)
display_off          = const(0x0A)
cursor_on            = const(0x0A)
cursor_off           = const(0x08)
blink_on             = const(0x09)
blink_off            = const(0x08)
                                    
_8_pin_interface     = const(0x30)
_4_pin_interface     = const(0x20)
_2_row_display       = const(0x28)
_1_row_display       = const(0x20)
_5x10_dots           = const(0x60)
_5x7_dots            = const(0x20)

line_1_y_pos         = const(0x00)
line_2_y_pos         = const(0x40)
line_3_y_pos         = const(0x14)
line_4_y_pos         = const(0x54)

BL_ON                = True
BL_OFF               = False

DAT                  = True
CMD                  = False


class LCD():        
    def __init__(self):
        self.init()
        
    
    def init(self):
        self.bl_state = BL_ON
        self.lcd_byte |= 0x04        
        self.write_byte(self.lcd_byte)
        sleep_ms(10)
        
        self.send_data(0x33, CMD)
        self.send_data(0x32, CMD)
        self.send_data((_4_pin_interface | _2_row_display | _5x7_dots), CMD)
        self.send_data((display_on | cursor_off | blink_off), CMD)
        self.send_data(clear_display, CMD)
        self.send_data((cursor_direction_inc | display_no_shift), CMD)
        self.clr_home()
        
        
    def send_data(self, send_value, mode):               
        if(mode == CMD):
            self.lcd_byte &= 0xF4
        else:
            self.lcd_byte |= 0x01
            
        if(self.bl_state == BL_ON):
            self.lcd_byte |= 0x08
        else:
            self.lcd_byte &= 0xF7
            
        self.write_byte(self.lcd_byte)
        self.quad_bit_send(send_value)
        
        
    def toggle_EN(self):
        self.lcd_byte |= 0x04
        self.write_byte(self.lcd_byte)
        sleep_ms(2)
        self.lcd_byte &= 0xF9
        self.write_byte(self.lcd_byte)
        sleep_ms(2)


    def quad_bit_send(self, lcd_data):        
        temp = (lcd_data & 0xF0)
        self.lcd_byte &= 0x0F
        self.lcd_byte |= temp
        self.write_byte(self.lcd_byte)
        self.toggle_EN()
        
        temp = (lcd_data & 0x0F)
        temp <<= 0x04
        self.lcd_byte &= 0x0F
        self.lcd_byte |= temp
        self.write_byte(self.lcd_byte)
        self.toggle_EN()
        
        
    def clr_home(self):        
        self.send_data(clear_display, CMD)
        self.send_data(goto_home, CMD)
        
        
    def goto_xy(self, x_pos, y_pos):        
        if(y_pos == 0):
            self.send_data((0x80 | x_pos), CMD)
        else:
            self.send_data((0xC0 | x_pos), CMD)
           
           
    def put_chr(self, ch):        
        self.send_data(ord(ch), DAT)
        
        
    def put_str(self, ch_string, x_pos, y_pos):        
        for character in ch_string:
            self.put_chr(character)
            
            
    def text(self, ch_string, x_pos, y_pos):        
        for character in ch_string:
            self.goto_xy(x_pos, y_pos)
            self.put_chr(character)
            x_pos += 1
            
            
class TWI_LCD(LCD):    
    def __init__(self, _i2c, _i2c_addr = default_I2C_address):
        self.io_ex = 0x00
        self.lcd_byte = 0x00
        self.bl_state = 0x00
        
        self.i2c = _i2c
        self.i2c_addr = _i2c_addr
        
        super().__init__()
        

    def write_byte(self, value):
        self.i2c.writeto(self.i2c_addr, bytes([value]))
        
        
    def read_byte(self, mask):        
        self.write_byte(mask)
        retval = self.i2c.readfrom(self.i2c_addr, 1)        
        return retval[0]


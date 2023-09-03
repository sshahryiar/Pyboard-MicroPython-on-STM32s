from micropython import const
import framebuf


SH1107_I2C_address = const(0x3C)


SH1107_SET_LOWER_COLUMN_ADDRESS = const(0x00)
SH1107_SET_UPPER_COLUMN_ADDRESS = const(0x10)
SH1107_SET_PAGE_MEMORY_ADDRESSING_MODE = const(0x20)
SH1107_SET_VERTICAL_MEMORY_ADDRESSING_MODE = const(0x21)
SH1107_SET_CONSTRAST_CONTROL = const(0x81)
SH1107_SET_DC_DC_OFF_MODE = const(0x8A)
SH1107_SET_DC_DC_ON_MODE = const(0x8B)
SH1107_SET_SEGMENT_REMAP_NORMAL = const(0xA0)
SH1107_SET_SEGMENT_REMAP_REVERSE = const(0xA1)
SH1107_SET_ENTIRE_DISPLAY_OFF = const(0xA4)
SH1107_SET_ENTIRE_DISPLAY_ON = const(0xA5)
SH1107_SET_NORMAL_DISPLAY = const(0xA6)
SH1107_SET_REVERSE_DISPLAY = const(0xA7)
SH1107_SET_MULTIPLEX_RATIO = const(0xA8)
SH1107_SET_DC_DC_CONTROL_MODE = const(0xAD)
SH1107_DISPLAY_OFF = const(0xAE)
SH1107_DISPLAY_ON = const(0xAF)
SH1107_SET_PAGE_ADDRESS = const(0xB0)
SH1107_SET_COMMON_OUTPUT_SCAN_DIRECTION = const(0xC0)
SH1107_SET_DISPLAY_OFFSET = const(0xD3)
SH1107_SET_DISPLAY_CLOCK_FREQUENCY = const(0xD5)
SH1107_SET_PRECHARGE_DISCHARGE_PERIOD = const(0xD9)
SH1107_SET_VCOM_DESELECT_LEVEL = const(0xDB)
SH1107_SET_DISPLAY_START_LINE = const(0xDC)


disp_width = const(128)
disp_height = const(64)
disp_pages = const((disp_height >> 3))


class OLED(framebuf.FrameBuffer):
    
    def __init__(self, _i2c, _i2c_address = SH1107_I2C_address):
        self.width = disp_width
        self.height = disp_height
        self.pages = disp_pages
        
        self.line_bytes = (self.width >> 3)
        size = (self.width * self.pages)
        self.curr_buffer = bytearray(b'\x00' * size) 
        self.prev_buffer = bytearray(b'\xFF' * size)
        
        self.write_list = [b"\x40", None]   
        self.temp = bytearray(0x02)
        
        self.WHITE = 1
        self.BLACK = 0
        
        self.i2c = _i2c
        self.i2c_addr = _i2c_address
                
        super().__init__(self.curr_buffer, self.width, self.height, framebuf.MONO_HMSB)
        self.init_display()
        
        
    def write_command(self, cmd):
        self.temp[0] = 0x80  
        self.temp[1] = cmd
        self.i2c.writeto(self.i2c_addr, self.temp)

    
    def write_data(self, data_buffer):
        self.write_list[1] = data_buffer
        self.i2c.writevto(self.i2c_addr, self.write_list)


    def init_display(self):
        self.write_command(SH1107_DISPLAY_OFF)

        self.write_command(SH1107_SET_LOWER_COLUMN_ADDRESS)  
        self.write_command(SH1107_SET_UPPER_COLUMN_ADDRESS)   

        self.write_command(SH1107_SET_PAGE_ADDRESS)
      
        self.write_command(SH1107_SET_DISPLAY_START_LINE)     
        self.write_command(0x00) 
        self.write_command(SH1107_SET_CONSTRAST_CONTROL)   
        self.write_command(0x44)    
        self.write_command(SH1107_SET_VERTICAL_MEMORY_ADDRESSING_MODE) 
    
        self.write_command(SH1107_SET_SEGMENT_REMAP_REVERSE)   
        self.write_command(SH1107_SET_COMMON_OUTPUT_SCAN_DIRECTION)    
        self.write_command(SH1107_SET_ENTIRE_DISPLAY_OFF)   

        self.write_command(SH1107_SET_NORMAL_DISPLAY)   
        self.write_command(SH1107_SET_MULTIPLEX_RATIO)   
        self.write_command(0x7F)   
  
        self.write_command(SH1107_SET_DISPLAY_OFFSET)    
        self.write_command(0x60)

        self.write_command(SH1107_SET_DISPLAY_CLOCK_FREQUENCY)    
        self.write_command(0x81)
    
        self.write_command(SH1107_SET_PRECHARGE_DISCHARGE_PERIOD)   
        self.write_command(0x22)   

        self.write_command(SH1107_SET_VCOM_DESELECT_LEVEL)   
        self.write_command(0x35)  
    
        self.write_command(SH1107_SET_DC_DC_CONTROL_MODE)    
        self.write_command(SH1107_SET_DC_DC_OFF_MODE)    
        self.write_command(SH1107_DISPLAY_ON)
        
        
    def modify_buf(self, offs, width):
        ptr = offs
        width += offs
        while(ptr < width):
            while((ptr < width) and (self.curr_buffer[ptr : (ptr + 0x08)] == self.prev_buffer[ptr : (ptr + 0x08)])):
                ptr += 0x08

            if(ptr < width):
                first = ptr
                ptr += 0x08
                while((ptr < width) and (self.curr_buffer[ptr : (ptr + 0x08)] != self.prev_buffer[ptr : (ptr + 0x08)])):
                    ptr += 0x08

                yield first, ptr
                ptr += 0x08

  
    def show(self):
        for col in range(self.height):
            noffs = (col * self.line_bytes)
            for page1, page2 in self.modify_buf(noffs, self.line_bytes):
                self.write_command(SH1107_SET_PAGE_ADDRESS | (page1 - noffs))
                self.write_command(SH1107_SET_LOWER_COLUMN_ADDRESS | (col & 0x0F))
                self.write_command(SH1107_SET_UPPER_COLUMN_ADDRESS | ((col & 0x70) >> 0x04))
                self.write_data(self.curr_buffer[page1 : page2])
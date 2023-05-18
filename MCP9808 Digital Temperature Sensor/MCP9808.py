from micropython import const
from machine import I2C


MCP9808_I2C_address = const(0x18)

MCP9808_CONFIG_REG = const(0x01) 
MCP9808_UPPER_TEMP_REG = const(0x02)
MCP9808_LOWER_TEMP_REG = const(0x03)
MCP9808_CRITICAL_TEMP_REG = const(0x04)
MCP9808_AMBIENT_TEMP_REG = const(0x05)
MCP9808_MANUFACTURER_ID_REG = const(0x06)
MCP9808_DEVICE_ID_REG = const(0x07)
MCP9808_RESOLUTION_REG = const(0x08)


class MCP9808():
    
    def __init__(self):
        self.i2c = I2C(2, freq = 400000)
        self.init()
        
        
    def write_byte(self, reg, value):
        if not type(value) is bytearray:
            value = bytearray([value])
           
        self.i2c.writeto_mem(MCP9808_I2C_address, reg, value)
    
    
    def write_word(self, reg, value):
        value = value & 0xFFFF
        arr = bytearray(0x02)
        arr[1] = (value & 0xFF)
        arr[0] = ((value >> 8) & 0xFF)
        
        self.i2c.writeto_mem(MCP9808_I2C_address, reg, arr)
    
        
    def read_byte(self, reg):
        retval = self.i2c.readfrom_mem(MCP9808_I2C_address, reg, 0x01)    
        return retval[0x00]
    
    
    def read_word(self, reg):
        value = self.i2c.readfrom_mem(MCP9808_I2C_address, reg, 0x02)
        retval = ((value[0x00] << 0x08) | value[0x01])
        return retval
    
    
    def init(self):
        manufacturer_ID = self.read_word(MCP9808_MANUFACTURER_ID_REG)       
        device_ID = self.read_word(MCP9808_DEVICE_ID_REG)
        
        if(manufacturer_ID == 0x0054):
            if(device_ID == 0x400):
                print("MCP9808 detected.")
                self.write_word(MCP9808_CONFIG_REG, 0x060E)
                self.write_word(MCP9808_RESOLUTION_REG, 0x0003)
            else:
                print("Issue with I2C device/bus!")
        else:
            print("MCP9808 not present.")
                

    def read_T_and_status(self):
        t = self.read_word(MCP9808_AMBIENT_TEMP_REG)
        status = ((t & 0xE000) >> 13)
        
        hb = ((t & 0x0F00) >> 8)
        lb = (t & 0x00FF)
        tmp = ((hb * 16.0) + (lb / 16.0))

        if(t & 0x1000):
            tmp = (256 - tmp)     
        
        return tmp, status
    
    
    def read_set_point(self, reg):
        ts = self.read_word(reg)
        
        if(ts != 0xFFFF):
            tmp = (ts & 0x0FFC)
            tmp >>= 2
            
            if(ts & 0x1000):
                tmp = (tmp - 1024)
                        
            tmp *= 0.25
            
        return tmp
    
    
    def read_T_upper(self):
        return self.read_set_point(MCP9808_UPPER_TEMP_REG)
    
    
    def read_T_lower(self):
        return self.read_set_point(MCP9808_LOWER_TEMP_REG)
    
    
    def read_T_critical(self):
        return self.read_set_point(MCP9808_CRITICAL_TEMP_REG)
    
    
    def write_set_point(self, reg, value):
        regval = int(16.0 * value)

        if(value < 0):
            regval |= 0x1000
            
        self.write_word(reg, regval)
            
            
    def set_T_upper(self, value):
        self.write_set_point(MCP9808_UPPER_TEMP_REG, value)
    
    
    def set_T_lower(self, value):
        self.write_set_point(MCP9808_LOWER_TEMP_REG, value)
    
    
    def set_T_critical(self, value):
        self.write_set_point(MCP9808_CRITICAL_TEMP_REG, value)
        
        
        
    
     
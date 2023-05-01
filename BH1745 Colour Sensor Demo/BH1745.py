from micropython import const
from machine import I2C


BH1745_I2C_address = const(0x38)

BH1745_SYSTEM_CONTROL_REG = const(0x40)
BH1745_MODE_CONTROL1_REG = const(0x41)
BH1745_MODE_CONTROL2_REG = const(0x42)
BH1745_MODE_CONTROL3_REG = const(0x44)
BH1745_RED_DATA_LSBs_REG = const(0x50)
BH1745_RED_DATA_MSBs_REG = const(0x51)
BH1745_GREEN_DATA_LSBs_REG = const(0x52)
BH1745_GREEN_DATA_MSBs_REG = const(0x53)
BH1745_BLUE_DATA_LSBs_REG = const(0x54)
BH1745_BLUE_DATA_MSBs_REG = const(0x55)
BH1745_CLEAR_DATA_LSBs_REG = const(0x56)
BH1745_CLEAR_DATA_MSBs_REG = const(0x57)
BH1745_DINT_DATA_LSBs_REG = const(0x58)
BH1745_DINT_DATA_MSBs_REG = const(0x59)
BH1745_INTERRUPT_REG = const(0x60)
BH1745_PERSISTENCE_REG = const(0x61)
BH1745_TH_LSBs_REG = const(0x62)
BH1745_TH_MSBs_REG = const(0x63)
BH1745_TL_LSBs_REG = const(0x64)
BH1745_TL_MSBs_REG = const(0x65)
BH1745_MANUFACTURER_ID_REG = const(0x92)

BH1745_PART_ID = const(0x0B)

BH1745_SYSTEM_CONTROL_SW_RESET_ACTIVE = const(0x8B)
BH1745_SYSTEM_CONTROL_SW_RESET_INACTIVE = const(0x0B)
BH1745_SYSTEM_CONTROL_INT_PIN_ACTIVE = const(0x4B)
BH1745_SYSTEM_CONTROL_INT_PIN_INACTIVE = const(0x0B)

BH1745_MODE_CONTROL1_MEASUREMENT_TIME_160ms = const(0x00)
BH1745_MODE_CONTROL1_MEASUREMENT_TIME_320ms = const(0x01)
BH1745_MODE_CONTROL1_MEASUREMENT_TIME_640ms = const(0x02)
BH1745_MODE_CONTROL1_MEASUREMENT_TIME_1280ms = const(0x03)
BH1745_MODE_CONTROL1_MEASUREMENT_TIME_2560ms = const(0x04)
BH1745_MODE_CONTROL1_MEASUREMENT_TIME_5120ms = const(0x05)

BH1745_MODE_CONTROL2_RGBC_MEASUREMENT_ACTIVE = const(0x10)
BH1745_MODE_CONTROL2_RGBC_MEASUREMENT_INACTIVE = const(0x00)
BH1745_MODE_CONTROL2_ADC_GAIN_1X = const(0x00)
BH1745_MODE_CONTROL2_ADC_GAIN_2X = const(0x01)
BH1745_MODE_CONTROL2_ADC_GAIN_16X = const(0x02)

BH1745_MODE_CONTROL3_BYTE = const(0x02)

BH1745_INTERRUPT_INT_LATCHED = const(0x00)
BH1745_INTERRUPT_INT_NOT_LATCHED = const(0x10)
BH1745_INTERRUPT_INT_SOURCE_RED_CHANNEL = const(0x00)
BH1745_INTERRUPT_INT_SOURCE_GREEN_CHANNEL = const(0x04)
BH1745_INTERRUPT_INT_SOURCE_BLUE_CHANNEL = const(0x08)
BH1745_INTERRUPT_INT_SOURCE_CLEAR_CHANNEL = const(0x0C)
BH1745_INTERRUPT_INT_ENABLED = const(0x01)
BH1745_INTERRUPT_INT_DISABLED = const(0x00)

BH1745_PERSISTENCE_CASE1 = const(0x00)
BH1745_PERSISTENCE_CASE2 = const(0x01)
BH1745_PERSISTENCE_CASE3 = const(0x02)
BH1745_PERSISTENCE_CASE4 = const(0x03)

BH1745_MANUFACTURER_ID = const(0xE0)


class BH1745():

    def __init__(self):
        self.i2c = I2C(1, freq = 400000)
        self.init()


    def init(self):
        part_id = self.read_byte(BH1745_SYSTEM_CONTROL_REG)

        if(part_id != BH1745_PART_ID):
            print("Error! Wrong/Damaged Part!")
        else:
            print("Found BH1745....")
            self.write(BH1745_MODE_CONTROL1_REG, BH1745_MODE_CONTROL1_MEASUREMENT_TIME_320ms)
            self.write(BH1745_MODE_CONTROL2_REG, (BH1745_MODE_CONTROL2_RGBC_MEASUREMENT_ACTIVE | BH1745_MODE_CONTROL2_ADC_GAIN_1X))
            self.write(BH1745_MODE_CONTROL3_REG, BH1745_MODE_CONTROL3_BYTE)
            self.write(BH1745_INTERRUPT_REG, (BH1745_INTERRUPT_INT_LATCHED | BH1745_INTERRUPT_INT_SOURCE_CLEAR_CHANNEL | BH1745_INTERRUPT_INT_DISABLED))
            self.write(BH1745_PERSISTENCE_REG, BH1745_PERSISTENCE_CASE1)
            manufacturer_id = self.read_byte(BH1745_MANUFACTURER_ID_REG)

            if(manufacturer_id == BH1745_MANUFACTURER_ID):
                print("Part matched. All set.")



    def write(self, reg, value):
        if not type(value) is bytearray:
            value = bytearray([value])
        
        self.i2c.writeto_mem(BH1745_I2C_address, reg, value)
        
        
    def read_byte(self, reg):
        retval = self.i2c.readfrom_mem(BH1745_I2C_address, reg, 0x01)    
        return retval[0x00]
    
    
    def read_word(self, reg):
        value = self.i2c.readfrom_mem(BH1745_I2C_address, reg, 0x02)
        retval = ((value[0x01] << 0x08) | value[0x00])
        return retval


    def read_RGBC(self):
        r = 0
        g = 0
        b = 0
        c = 0
        rgb = 0
        
    	r = self.read_byte(BH1745_RED_DATA_LSBs_REG)
    	g = self.read_byte(BH1745_GREEN_DATA_LSBs_REG)
    	b = self.read_byte(BH1745_BLUE_DATA_LSBs_REG)
    	c = self.read_byte(BH1745_CLEAR_DATA_LSBs_REG)
    	rgb = (((r << 16) | (g << 8) | b) & 0xFFFF)
    	
    	return r, g, b, c, rgb


    def RGB_to_HSV(self):
    	R, G, B, C, RGB = self.read_RGBC()

    	r_ch = (R / 65535.0)
    	g_ch = (G / 65535.0)
    	b_ch = (B / 65535.0)

    	max_R_vs_G = max(r_ch, g_ch)
    	max_RG_vs_B = max(max_R_vs_G, b_ch)

    	min_R_vs_G = min(r_ch, g_ch)
    	min_RG_vs_B = min(max_R_vs_G, b_ch)

    	diff = (max_RG_vs_B - min_RG_vs_B)

    	if(diff == 0):
    		hue = 0

    	elif(max_RG_vs_B == r_ch):
    		if(g_ch >= b_ch):
    			hue = (60 * ((g_ch - b_ch) / diff + 0))
    		else:
    			hue = (60 * ((g_ch - b_ch) / diff + 6))

    	elif(max_RG_vs_B == g_ch):
    		hue = (60 * ((b_ch - r_ch) / diff + 2))

    	elif(max_RG_vs_B == b_ch):
    		hue = (60 * ((r_ch - g_ch) / diff + 2))

    	brightness = ((max_RG_vs_B + min_RG_vs_B) * 0.5)

    	if(brightness == 0):
    		saturation = 0

    	elif(brightness <= 0.5):
    		saturation = (diff / (brightness * 2))

    	else:
    		saturation = (diff / (2 - (brightness * 2)))


    	return hue, saturation, brightness



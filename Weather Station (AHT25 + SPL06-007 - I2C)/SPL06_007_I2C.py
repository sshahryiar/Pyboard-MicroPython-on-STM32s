from micropython import const
from utime import sleep_ms


SPL06_I2C_default_address = const(0x76)

SPL06_PSR_B2_REG = const(0x00)
SPL06_PSR_B1_REG = const(0x01)
SPL06_PSR_B0_REG = const(0x02)
SPL06_TMP_B2_REG = const(0x03)
SPL06_TMP_B1_REG = const(0x04)
SPL06_TMP_B0_REG = const(0x05)
SPL06_PRS_CFG_REG = const(0x06)
SPL06_TMP_CFG_REG = const(0x07)
SPL06_MEAS_CFG_REG = const(0x08)
SPL06_CFG_REG = const(0x09)
SPL06_INT_STS_REG = const(0x0A)
SPL06_FIFO_STS_REG = const(0x0B)
SPL06_RESET_REG = const(0x0C)
SPL06_ID_REG = const(0x0D)
SPL06_COEF_c0_REG = const(0x10)
SPL06_COEF_c0_1_REG = const(0x11)
SPL06_COEF_c1_REG = const(0x12)
SPL06_COEF_c00_A_REG = const(0x13)
SPL06_COEF_c00_B_REG = const(0x14)
SPL06_COEF_c00_10_REG = const(0x15)
SPL06_COEF_c10_A_REG = const(0x16)
SPL06_COEF_c10_B_REG = const(0x17)
SPL06_COEF_c01_A_REG = const(0x18)
SPL06_COEF_c01_B_REG = const(0x19)
SPL06_COEF_c11_A_REG = const(0x1A)
SPL06_COEF_c11_B_REG = const(0x1B)
SPL06_COEF_c20_A_REG = const(0x1C)
SPL06_COEF_c20_B_REG = const(0x1D)
SPL06_COEF_c21_A_REG = const(0x1E)
SPL06_COEF_c21_B_REG = const(0x1F)
SPL06_COEF_c30_A_REG = const(0x20)
SPL06_COEF_c30_B_REG = const(0x21)


class SPL06():
    
    def __init__(self, _i2c, _i2c_address = SPL06_I2C_default_address):
        self.i2c = _i2c
        self.i2c_address = _i2c_address
        
        self.init()
        
        
    def init(self):
        self.write(SPL06_PRS_CFG_REG, 0x03)
        self.write(SPL06_TMP_CFG_REG, 0x83)
        self.write(SPL06_MEAS_CFG_REG, 0x07)
        self.write(SPL06_CFG_REG, 0x00)
        
        
    def write(self, address, value):
        if not type(value) is bytearray:
            value = bytearray([value])
        
        self.i2c.writeto_mem(self.i2c_address, address, value)
        
        
    def read_byte(self, address):
        value = 0
        retval = self.i2c.readfrom_mem(self.i2c_address, address, 1)    
        return retval[0]
    
    
    def get_ID(self):
        return self.read_byte(SPL06_ID_REG)
    
    
    def get_prs_config(self):
        return self.read_byte(SPL06_PRS_CFG_REG)
    
    
    def get_tmp_config(self):
        return self.read_byte(SPL06_TMP_CFG_REG)
    
    
    def get_measure_config(self):
        return self.read_byte(SPL06_MEAS_CFG_REG)
    
    
    def get_config_reg(self):
        return self.read_byte(SPL06_CFG_REG)
    
    
    def get_int_status(self):
        return self.read_byte(SPL06_INT_STS_REG)
    
    
    def get_FIFO_status(self):
        return self.read_byte(SPL06_FIFO_STS_REG)
    
    
    def two_complement(self, value, bits):
        if((value & (1 << (bits - 1))) != 0):
            value = (value - (1 << bits))
            
        return value

        
        
    def get_C0(self):
        HB = 0
        LB = 0
        temp = 0
        
        HB = self.read_byte(SPL06_COEF_c0_REG)
        LB = self.read_byte(SPL06_COEF_c0_1_REG)
        
        LB >>= 4
        
        temp = ((HB << 4) | LB)
        temp = self.two_complement(temp, 12)
        
        return temp
    
    
    def get_C1(self):
        HB = 0
        LB = 0
        temp = 0
        
        HB = self.read_byte(SPL06_COEF_c0_1_REG)
        LB = self.read_byte(SPL06_COEF_c1_REG)
        
        HB &= 0x0F
        
        temp = ((HB << 8) | LB)        
        temp = self.two_complement(temp, 12)
        
        return temp
    
    
    def get_C00(self):
        byte_1 = 0
        byte_2 = 0
        byte_3 = 0
        temp = 0

        byte_1 = self.read_byte(SPL06_COEF_c00_A_REG)
        byte_2 = self.read_byte(SPL06_COEF_c00_B_REG)
        byte_3 = self.read_byte(SPL06_COEF_c00_10_REG)

        temp = ((byte_1 << 12) | (byte_2 << 4) | (byte_3 >> 4))
        temp = self.two_complement(temp, 20)
        
        return temp
    
    
    def get_C10(self):
        byte_1 = 0
        byte_2 = 0
        byte_3 = 0
        temp = 0

        byte_1 = self.read_byte(SPL06_COEF_c00_10_REG)
        byte_2 = self.read_byte(SPL06_COEF_c10_A_REG)
        byte_3 = self.read_byte(SPL06_COEF_c10_B_REG)
        
        byte_1 &= 0x0F

        temp = ((byte_1 << 16) | (byte_2 << 8) | byte_3)
        temp = self.two_complement(temp, 20)
        
        return temp 
    
    
    def get_C01(self):
        HB = 0
        LB = 0
        temp = 0
        
        HB = self.read_byte(SPL06_COEF_c01_A_REG)
        LB = self.read_byte(SPL06_COEF_c01_B_REG)
        
        temp = ((HB << 8) | LB)
        temp = self.two_complement(temp, 16)
        
        return temp
    

    def get_C11(self):
        HB = 0
        LB = 0
        temp = 0
        
        HB = self.read_byte(SPL06_COEF_c11_A_REG)
        LB = self.read_byte(SPL06_COEF_c11_B_REG)
        
        temp = ((HB << 8) | LB)
        temp = self.two_complement(temp, 16)
        
        return temp
    
    
    def get_C20(self):
        HB = 0
        LB = 0
        temp = 0
        
        HB = self.read_byte(SPL06_COEF_c20_A_REG)
        LB = self.read_byte(SPL06_COEF_c20_B_REG)
        
        temp = ((HB << 8) | LB)
        temp = self.two_complement(temp, 16)
        
        return temp
    
    
    def get_C21(self):
        HB = 0
        LB = 0
        temp = 0
        
        HB = self.read_byte(SPL06_COEF_c21_A_REG)
        LB = self.read_byte(SPL06_COEF_c21_B_REG)
        
        temp = ((HB << 8) | LB)
        temp = self.two_complement(temp, 16)
        
        return temp
    
    
    def get_C30(self):
        HB = 0
        LB = 0
        temp = 0
        
        HB = self.read_byte(SPL06_COEF_c30_A_REG)
        LB = self.read_byte(SPL06_COEF_c30_B_REG)
        
        temp = ((HB << 8) | LB)     
        temp = self.two_complement(temp, 16)
        
        return temp
    
    
    def get_scale_factor(self, t_or_p):
        temp = 0
        temp_byte = 0
        
        if(t_or_p == True):
            temp_byte = self.get_tmp_config()
            
        else:
            temp_byte = self.get_prs_config()
        
        temp_byte &= 0x07
        
        if(temp_byte == 0x00):
            temp = 524288.0
            
        elif(temp_byte == 0x01):
            temp = 1572864.0
            
        elif(temp_byte == 0x02):
            temp = 3670016.0
    
        elif(temp_byte == 0x03):
            temp = 7864320.0
            
        elif(temp_byte == 0x04):
            temp = 253952.0
            
        elif(temp_byte == 0x05):
            temp = 516096.0
            
        elif(temp_byte == 0x06):
            temp = 1040384.0
            
        else:
            temp = 2088960.0
            
        return temp
    
    
    def get_tmp_raw(self):
        temp = 0
        byte_1 = 0
        byte_2 = 0
        byte_3 = 0
        
        byte_1 = self.read_byte(SPL06_TMP_B2_REG)
        byte_2 = self.read_byte(SPL06_TMP_B1_REG)
        byte_3 = self.read_byte(SPL06_TMP_B0_REG)
        
        temp = ((byte_1 << 8) | byte_2)
        temp = ((temp << 8) | byte_3)

        temp = self.two_complement(temp, 24)
        
        return temp
    
    
    def get_raw_scaled_tmp(self):
        raw_ST = self.get_tmp_raw()
        raw_ST /= self.get_scale_factor(True)
        
        return raw_ST
    
    
    def get_tmp(self):
        c0 = self.get_C0()
        c1 = self.get_C1()
        raw_t = self.get_raw_scaled_tmp()
        temp = ((c0 * 0.5) + (c1 * raw_t))
        
        return temp
    
    
    def get_prs_raw(self):
        temp = 0
        byte_1 = 0
        byte_2 = 0
        byte_3 = 0
        
        byte_1 = self.read_byte(SPL06_PSR_B2_REG)
        byte_2 = self.read_byte(SPL06_PSR_B1_REG)
        byte_3 = self.read_byte(SPL06_PSR_B0_REG)
        
        temp = ((byte_1 << 8) | byte_2)
        temp = ((temp << 8) | byte_3)

        temp = self.two_complement(temp, 24)
        
        return temp
    
    
    def get_raw_scaled_prs(self):
        raw_SP = self.get_prs_raw()
        raw_SP /= self.get_scale_factor(False)
        
        return raw_SP
    
    
    def get_compensated_prs(self):
        c00 = self.get_C00()
        c10 = self.get_C10()
        c01 = self.get_C01()
        c11 = self.get_C11()
        c20 = self.get_C20()
        c21 = self.get_C21()
        c30 = self.get_C30()
        
        scaled_prs_raw = self.get_raw_scaled_prs()
        scaled_tmp_raw = self.get_raw_scaled_tmp()
        
        comp_prs = (c00 +
                    (scaled_prs_raw * (c10 + (scaled_prs_raw * (c20 + (scaled_prs_raw * c30)))) +
                     (scaled_tmp_raw * c01) +
                     (scaled_prs_raw * scaled_tmp_raw * (c11 + (scaled_prs_raw * c21)))))
        
        return comp_prs
    
    
    def get_prs(self):
        temp = self.get_compensated_prs()
        temp /= 100.0
        
        return temp
        
    
        
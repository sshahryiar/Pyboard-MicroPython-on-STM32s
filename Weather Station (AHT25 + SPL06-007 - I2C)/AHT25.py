from micropython import const
from utime import sleep_ms


AHT25_I2C_Address = const(0x38)

AHT25_INIT_CMD = const(0xE1)
AHT25_TRIGGER_MEASURMENT_CMD = const(0xAC)
AHT25_SOFT_RESET_CMD = const(0xBA)

AHT25_INIT_CAL_ENABLE = const(0x08)
AHT25_DATA_MEASURMENT_CMD = const(0x33)
AHT25_DATA_NOP = const(0x00)


class AHT25():
    
    def __init__(self, _i2c):
        self.i2c = _i2c
        self.i2c_address = AHT25_I2C_Address
        
        self.buf = bytearray(0x07)
        for i in range(0, 7):
            self.buf[i] = 0x00
        
        self.init()
        
    
    def init(self):
        self.soft_reset()
        self.calibrate()
        sleep_ms(200)
        
        
    def write_bytes(self, cmd_1, cmd_2):
        self.buf[0] = cmd_1
        self.buf[1] = cmd_2
        self.buf[2] = AHT25_DATA_NOP
        
        self.i2c.writeto(self.i2c_address, self.buf[0:3])


    def read_sensor(self):
        t = 0
        rh = 0
        crc = 0
        status = 0
        self.write_bytes(AHT25_TRIGGER_MEASURMENT_CMD, AHT25_DATA_MEASURMENT_CMD)
        sleep_ms(10)
        value = self.i2c.readfrom_into(self.i2c_address, self.buf, 0x07)
        
        status = self.buf[0]
        rh = ((self.buf[1] << 12) | (self.buf[2] << 4) | (self.buf[3] >> 4))
        t = (((self.buf[3] & 0x0F) << 16) | (self.buf[4] << 8) | (self.buf[5]))
        crc = self.buf[6]
        
        rh = ((rh * 100.0) / 0x100000)
        t = (((t * 200.0) / 0x100000) - 50.0)
        
        return rh, t, status, crc
    
    
    def calibrate(self):
        self.write_bytes(AHT25_INIT_CMD, AHT25_INIT_CAL_ENABLE)
        sleep_ms(600)
        
        
    def soft_reset(self):
        self.buf[0] = AHT25_SOFT_RESET_CMD
        self.i2c.writeto(self.i2c_address, self.buf[0:1])
        sleep_ms(200)
from micropython import const
from utime import sleep_ms


class MODBUS_DS18B20():
    def __init__(self, _uart):
        self.tx_data_frame = bytearray(8)
        self.rx_data_frame = bytearray(9)
        
        self.uart = _uart

    
    def generate_CRC16(self, value, length):
        n = 0
        s = 0
        crc_word = 0xFFFF
        
        for s in range (0x00, length):
            crc_word ^= value[s]
            
            for n in range (0x00, 0x08):
                if((crc_word & 0x0001) == 0):
                    crc_word >>= 1
                
                else:
                    crc_word >>= 1
                    crc_word ^= 0xA001
        
        return crc_word
    
    
    def check_crc(self, value, s, e):
        hb = value[e]
        lb = value[s]
        crc = hb
        crc <<= 8
        crc |= lb
        
        return crc
    
    
    def MODBUS_RX(self):
        if(self.uart.any() > 0x00):
            self.rx_data_frame = self.uart.read(9)
    
    
    def MODBUS_TX(self):
        crc = 0
        self.tx_data_frame[0x00] = 0x01
        self.tx_data_frame[0x01] = 0x03
        self.tx_data_frame[0x02] = 0x00
        self.tx_data_frame[0x03] = 0x00
        self.tx_data_frame[0x04] = 0x00
        self.tx_data_frame[0x05] = 0x02
        
        crc = self.generate_CRC16(self.tx_data_frame, 6)
        
        self.tx_data_frame[0x06] = (crc & 0x00FF)
        self.tx_data_frame[0x07] = ((crc & 0xFF00) >> 0x08)
        
        self.uart.write(self.tx_data_frame)
        sleep_ms(100)
        
    
    def get_temp(self):
        crc_1 = 0x0000
        crc_2 = 0xFFFF
        temp = 1000      
        
        self.MODBUS_TX()
        self.MODBUS_RX()
        
        if(self.rx_data_frame[0x00] == 0x01):
            if(self.rx_data_frame[0x01] == 0x03):
                crc_1 = self.generate_CRC16(self.rx_data_frame, 7)
                crc_2 = self.check_crc(self.rx_data_frame, 7, 8)
                
                if(crc_1 == crc_2):
                    temp = self.rx_data_frame[3]
                    temp <<= 0x08
                    temp |= self.rx_data_frame[4]
                    temp /= 10.0
                    
                    if((temp >= -30) and (temp <= 110)):
                        return temp
                    else:
                        return -1000
                    
        return 1000


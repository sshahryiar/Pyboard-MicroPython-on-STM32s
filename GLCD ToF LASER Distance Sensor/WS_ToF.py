from micropython import const
from utime import sleep_ms, ticks_ms


ToF_TX_data_packet_size = const(32)
ToF_RX_data_packet_size = const(32)

ToF_output_frame_header = const(0x57)
ToF_output_function_mark = const(0x00)

ToF_inquire_function_mark = const(0x10)

ToF_settings_frame_header = const(0x54)
ToF_settings_function_mark = const(0x20)

Tof_output_mode_active = const(0x00)
Tof_output_mode_inquire = const(0x02)

Tof_output_range_mode_short = const(0x00)
Tof_output_range_mode_medium = const(0x08)
Tof_output_range_mode_long = const(0x04)

Tof_output_interface_UART = const(0x00)
Tof_output_interface_CAN = const(0x01)
Tof_output_interface_IO = const(0x10)
Tof_output_interface_I2C = const(0x11)

Tof_UART_Baud_115200 = const(115200)
Tof_UART_Baud_230400 = const(230400)
Tof_UART_Baud_460800 = const(460800)
Tof_UART_Baud_921600 = const(921600)

Tof_CAN_Baud_1000000 = const(1000000)
Tof_CAN_Baud_1200000 = const(1200000)
Tof_CAN_Baud_1500000 = const(1500000)
Tof_CAN_Baud_2000000 = const(2000000)
Tof_CAN_Baud_3000000 = const(3000000)


class waveshare_ToF():
    
    def __init__(self, _uart):
        self.tx_data_frame = bytearray(ToF_TX_data_packet_size)
        self.rx_data_frame = bytearray(ToF_RX_data_packet_size)
        
        self.uart = _uart
        
        
    def settings(self,
                 ID = 0,
                 terminal_time = ticks_ms(),
                 mode = (Tof_output_mode_inquire | Tof_output_range_mode_long | Tof_output_interface_UART),
                 baud_rate = Tof_UART_Baud_115200,
                 band_start = 0,
                 bandwidth = 0):
        
        chk_sum = 0
        current_tick = terminal_time
        baud_value = baud_rate
        bs = band_start
        bw = bandwidth
        
        self.tx_data_frame[0] = ToF_settings_frame_header
        self.tx_data_frame[1] = ToF_settings_function_mark
        self.tx_data_frame[2] = 0
        self.tx_data_frame[3] = 0xFF
        self.tx_data_frame[4] = ID                
        self.tx_data_frame[5] = (current_tick & 0x000F)  
        self.tx_data_frame[6] = ((current_tick & 0x00F0) >> 8) 
        self.tx_data_frame[7] = ((current_tick & 0x0F00) >> 16) 
        self.tx_data_frame[8] = ((current_tick & 0xF000) >> 24) 
        self.tx_data_frame[9] = mode
        self.tx_data_frame[10] = 0xFF
        self.tx_data_frame[11] = 0xFF
        self.tx_data_frame[12] = (baud_value & 0x000F) 
        self.tx_data_frame[13] = ((baud_value & 0x00F0) >> 8) 
        self.tx_data_frame[14] = ((baud_value & 0x0F00) >> 16) 
        self.tx_data_frame[15] = 0xFF
        self.tx_data_frame[16] = 0xFF      
        self.tx_data_frame[17] = 0xFF    
        self.tx_data_frame[18] = 0xFF        
        self.tx_data_frame[19] = (bs & 0x000F)       
        self.tx_data_frame[20] = ((bs & 0x00F0) >> 8) 
        self.tx_data_frame[21] = (bw & 0x000F)       
        self.tx_data_frame[22] = ((bw & 0x00F0) >> 8)         
        self.tx_data_frame[23] = 0xFF
        self.tx_data_frame[24] = 0xFF      
        self.tx_data_frame[25] = 0xFF    
        self.tx_data_frame[26] = 0xFF
        self.tx_data_frame[27] = 0xFF
        self.tx_data_frame[28] = 0xFF      
        self.tx_data_frame[29] = 0xFF    
        self.tx_data_frame[30] = 0xFF
        
        for i in range(0, 31):
            chk_sum += self.tx_data_frame[i]
            
        self.tx_data_frame[31] = (chk_sum & 0xFF)
        
        self.uart.write(self.tx_data_frame)
        sleep_ms(60)
        
        chk_sum = 0
        current_tick = 0
        baud_value = 0
        bs = 0
        bw = 0
        
        if(self.uart.any() > 0x00):
            self.rx_data_frame = self.uart.read(ToF_RX_data_packet_size)
            
            if(self.rx_data_frame[0] == ToF_settings_frame_header):
                
                if(self.rx_data_frame[1] == ToF_settings_function_mark):
                    
                    if(self.rx_data_frame[2] == 1):
                         
                        ID = self.rx_data_frame[4]
                        current_tick = ((self.rx_data_frame[8] << 24) |
                                        (self.rx_data_frame[7] << 16) |
                                        (self.rx_data_frame[6] << 8) |
                                        self.rx_data_frame[5])
                        
                        mode = self.rx_data_frame[9]
                        baud_value = ((self.rx_data_frame[14] << 16) |
                                      (self.rx_data_frame[13] << 8) |
                                      self.rx_data_frame[12])
                        
                        bs = ((self.rx_data_frame[20] << 8) | 
                              self.rx_data_frame[19])
                        
                        bw = ((self.rx_data_frame[22] << 8) | 
                              self.rx_data_frame[21])

                        for i in range(0, 31):
                            chk_sum += self.rx_data_frame[i]
                            
                        chk_sum = (chk_sum & 0xFF)
                            
                        if(chk_sum == self.rx_data_frame[31]):
                            return ID, current_tick, mode, baud_value, bs, bw
                        
                        else:
                            return 0, 0, 0, 0, 0, 0
                        
        return -1, -1, -1, -1, -1, -1
    
    
    def inquire_sensor(self, ID = 0, delay = 60):
        chk_sum = 0
        
        self.tx_data_frame[0] = ToF_output_frame_header
        self.tx_data_frame[1] = ToF_inquire_function_mark
        self.tx_data_frame[2] = 0xFF
        self.tx_data_frame[3] = 0xFF
        self.tx_data_frame[4] = ID                
        self.tx_data_frame[5] = 0xFF 
        self.tx_data_frame[6] = 0xFF
        
        for i in range(0, 7):
            chk_sum += self.tx_data_frame[i]
        
        self.tx_data_frame[7] = chk_sum
        
        self.uart.write(self.tx_data_frame)
        sleep_ms(delay)
        
    
    
    def read_sensor(self, delay = 400):
        ID = 0
        sys_time = 0
        distance = 0
        status = 0
        sig_strength = 0
        precision = 0
        chk_sum = 0
        
        if(self.uart.any() > 0x00):
            self.rx_data_frame = self.uart.read(ToF_RX_data_packet_size)
            
            if(self.rx_data_frame[0] == ToF_output_frame_header):
                
                if(self.rx_data_frame[1] == ToF_output_function_mark):
                    
                    if(self.rx_data_frame[2] == 0xFF):
                        ID = self.rx_data_frame[3]
                        
                        sys_time = ((self.rx_data_frame[7] << 24) |
                                    (self.rx_data_frame[6] << 16) |
                                    (self.rx_data_frame[5] << 8) |
                                    self.rx_data_frame[4])
                        
                        distance = ((self.rx_data_frame[10] << 16) |
                                    (self.rx_data_frame[9] << 8) |
                                    self.rx_data_frame[8])
                        
                        
                        status = self.rx_data_frame[11]
                        sig_strength = ((self.rx_data_frame[13] << 8) |
                                        self.rx_data_frame[12]) 
                                                
                        precision = self.rx_data_frame[14]
                        
                        for i in range(0, 15):
                            chk_sum += self.rx_data_frame[i]
                            
                        chk_sum = (chk_sum & 0xFF)
                        sleep_ms(delay)
                        
                        if(chk_sum == self.rx_data_frame[15]):
                            return ID, sys_time, distance, status, sig_strength, precision
                        
                        else:
                            return 0, 0, 0, 0, 0, 0
                        
        sleep_ms(delay)                
        return -1, -1, -1, -1, -1, -1
                        
                        
                        
            
        
        
from pyb import LED, Pin, CAN
from machine import I2C
from micropython import const
from AHT20 import AHT20
from BMP280 import BMP280
from SSD1306_I2C import OLED1306
from utime import sleep_ms


node_ID = const(0x93)

rx_msg = 0
bmp_t = 0
bmp_p = 0
aht_t = 0
aht_rh = 0
aht_crc = 0
aht_status = 0
rx_node = 0
rx_data = 0
rx_data_frame = bytearray(6)
tx_data_frame = bytearray(6)


led = LED(4)
err_led = LED(1)

TWI_1 = I2C(1, freq = 400000)
TWI_2 = I2C(2, freq = 400000)


canbus = CAN(1, CAN.NORMAL)
canbus.setfilter(0, CAN.LIST16, 0, (0x66, 0x67, 0x68, 0x69))


pt = BMP280(TWI_2)
rht = AHT20(TWI_2)


def CAN_restart():
    global canbus
    canbus.deinit()
    canbus = CAN(1, CAN.NORMAL)
    canbus.clearfilter(0)
    canbus.setfilter(0, CAN.LIST16, 0, (0x66, 0x67, 0x68, 0x69))
    

oled = OLED1306(TWI_1)
oled.fill(oled.BLACK)
oled.show()


while(True):
    oled.fill(oled.BLACK)
    bmp_t = pt.get_temperature()
    bmp_p = pt.get_pressure()
    aht_rh, aht_t, aht_status, aht_crc = rht.read_sensor()
    t_avg = ((bmp_t + aht_t) / 2.0)
    
        
    oled.text("PYB CAN Node 2", 4, 1, oled.WHITE)
    oled.text(("TX Node: 0x" + str("%X " %node_ID)), 1, 10, oled.WHITE)
    oled.text((str("%3.1f" %t_avg) + "'C  " + str("%3.1f" %aht_rh) + "% "), 1, 20, oled.WHITE)
    oled.text((str("%4.1f" %bmp_p) + "mbar "), 1, 30, oled.WHITE)
         
    try:
        if(canbus.any(0)):
            rx_data_frame = canbus.recv(0)
        
        rx_node = rx_data_frame[0]
        rx_data = int.from_bytes(rx_data_frame[4], 'little')
        oled.text(("RX Node: 0x" + str("%X " %rx_node)), 1, 40, oled.WHITE)
        oled.text((str("%4u" %rx_data) + " lux "), 1, 50, oled.WHITE)
          
        err_led.off()
        
    except:
        CAN_restart()
        print("CAN BUS Receive Error!")
        err_led.on()
        
    
    try:

        lb = (int(bmp_p) & 0x00FF)
        hb = ((int(bmp_p) & 0xFF00) >> 8)
        
        tx_data_frame[0] = int(t_avg)
        tx_data_frame[1] = int(aht_rh)
        tx_data_frame[2] = hb
        tx_data_frame[3] = lb

        canbus.send(tx_data_frame, node_ID)
        
        
    except:
        CAN_restart()
        print("CAN BUS Transmit Error!")
        
    oled.show()
    led.toggle()
    sleep_ms(600)
from pyb import LED, Pin, CAN, ADC
from machine import I2C
from SSD1306_I2C import OLED1306
from utime import sleep_ms


rh = 0
lux = 0
prs = 0
tmp = 0
ID_1 = 0
ID_2 = 0
rx_node = 0
rx_data = bytearray(16)
rx_data_frame = bytearray(16)


err_led = LED(1)

TWI = I2C(1, freq = 100000) 


canbus = CAN(2, CAN.NORMAL)
canbus.setfilter(0, CAN.LIST16, 0, (0x66, 0x88, 0x93, 0x96))


def CAN_restart():
    global canbus
    canbus.deinit()
    canbus = CAN(2, CAN.NORMAL)
    canbus.clearfilter(0)
    canbus.setfilter(0, CAN.LIST16, 0, (0x66, 0x88, 0x93, 0x96))


oled = OLED1306(TWI)
oled.fill(oled.BLACK)
oled.show()


while(True):

    oled.fill(oled.BLACK)
    oled.text("PYB CAN Master", 8, 1, oled.WHITE)
    
    oled.text(("Node 1 ID: 0x" + str("%X " %ID_1)), 1, 10, oled.WHITE)
    oled.text(("Lux: " + str("%4u " %lux)), 1, 20, oled.WHITE)
    
    oled.text(("Node 2 ID: 0x" + str("%X " %ID_2)), 1, 30, oled.WHITE)
    oled.text((str("%3u" %tmp) + "'C  " + str("%3u" %rh) + "% "), 1, 40, oled.WHITE)
    oled.text((str("%4u" %prs) + " mbar "), 1, 50, oled.WHITE)
        
    try:
        if(canbus.any(0)):
            rx_data_frame = canbus.recv(0)
        
        rx_node = rx_data_frame[0]
        rx_data = rx_data_frame[3]
        
        if(rx_node == 0x66):
            ID_1 = rx_node
            lux = rx_data[0]
            
        elif(rx_node == 0x93):
            ID_2 = rx_node
            tmp = rx_data[0]
            rh = rx_data[1]
            prs = ((rx_data[2] << 8) | rx_data[3])
        
        err_led.off()
        
    except:
        CAN_restart()
        print("CAN BUS Error!")
        err_led.on()
        
    oled.show()
    sleep_ms(200)
    

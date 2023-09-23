from pyb import LED, Pin, CAN, ADC
from machine import I2C
from micropython import const
from SSD1306_I2C import OLED1306
from utime import sleep_ms


prs = 0
rx_node = 0
rx_data = bytearray(6)
rx_data_frame = bytearray(6)
tx_data_frame = bytearray(3)


node_ID = const(0x66)


led = LED(4)
err_led = LED(1)

TWI = I2C(1, freq = 400000)

adc= ADC(Pin("Y12"))

canbus = CAN(1, CAN.NORMAL)
canbus.setfilter(1, CAN.LIST16, 0, (0x90, 0x91, 0x92, 0x93))


oled = OLED1306(TWI)
oled.fill(oled.BLACK)
oled.show()


def CAN_restart():
    global canbus
    canbus.deinit()
    canbus = CAN(1, CAN.NORMAL)
    canbus.clearfilter(1)
    canbus.setfilter(1, CAN.LIST16, 0, (0x90, 0x91, 0x92, 0x93))
    


while(True):
    oled.fill(oled.BLACK)
    lux = (adc.read() >> 4) 
    oled.text("PYB CAN Node 1", 4, 1, oled.WHITE)
    oled.text(("TX Node: 0x" + str("%X " %node_ID)), 1, 10, oled.WHITE)
    oled.text(("Lux: " + str("%4u " %lux)), 1, 20, oled.WHITE)
    
    try:
        if(canbus.any(0)):
            rx_data_frame = canbus.recv(0)
        
        rx_node = rx_data_frame[0]
        rx_data = rx_data_frame[4]

        prs = ((rx_data[2] << 8) | rx_data[3])
        
        oled.text(("RX Node: 0x" + str("%X " %node_ID)), 1, 30, oled.WHITE)
        oled.text((str("%3u" %rx_data[0]) + "'C  " + str("%3u" %rx_data[1]) + "% "), 1, 40, oled.WHITE)
        oled.text((str("%4u" %prs) + " mbar "), 1, 50, oled.WHITE)

        err_led.off()
        
    except:
        print("CAN BUS Receive Error!")
        err_led.on()    
    
    try:
        CAN_restart()
        canbus.send(lux, node_ID)
        err_led.off()
        
    except:
        CAN_restart()
        print("CAN BUS Error!")
        err_led.on()
           
    oled.show()
    led.toggle()
    sleep_ms(400)
    
from pyb import LED
from machine import I2C
from SSD1306_I2C import OLED1306
from AHT25 import AHT25
from SPL06_007_I2C import SPL06
from utime import sleep_ms


shape_1 = [
[ 0, 0, 0, 0, 0, 0, 1, 0, 0],
[ 0, 1, 0, 0, 0, 0, 0, 1, 0],
[ 1, 0, 1, 0, 1, 1, 1, 1, 1],
[ 0, 0, 0, 1, 0, 0, 0, 1, 0],
[ 0, 0, 0, 0, 0, 0, 1, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 1, 0, 0, 0, 1, 0, 0, 0, 1],
[ 0, 1, 0, 1, 0, 1, 0, 1, 0],
[ 0, 0, 1, 0, 0, 0, 1, 0, 0],
]

shape_2 = [
[ 0, 0, 0, 0, 1, 0, 0, 0, 0],
[ 0, 0, 0, 0, 1, 0, 0, 0, 0],
[ 0, 0, 0, 1, 1, 1, 0, 0, 0],
[ 0, 0, 1, 1, 1, 1, 1, 0, 0],
[ 0, 1, 1, 1, 1, 1, 1, 1, 0],
[ 0, 1, 1, 1, 1, 1, 1, 1, 0],
[ 0, 1, 1, 1, 1, 1, 1, 1, 0],
[ 0, 0, 1, 1, 1, 1, 1, 0, 0],
[ 0, 0, 0, 1, 1, 1, 0, 0, 0],
]

shape_3 = [
[ 1, 0, 1, 0, 1, 0, 1, 0, 1],
[ 0, 1, 0, 1, 0, 1, 0, 1, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 1, 0, 0, 0, 1, 0, 0],
[ 0, 0, 1, 0, 0, 0, 1, 0, 0],
[ 0, 0, 1, 0, 0, 0, 1, 0, 0],
[ 0, 1, 1, 1, 0, 1, 1, 1, 0],
[ 0, 0, 1, 0, 0, 0, 1, 0, 0],
[ 1, 0, 1, 0, 1, 0, 1, 0, 1],
]


led = LED(1)

TWI = I2C(scl = 'PB9', sda = 'PB8', freq = 400000)

rht = AHT25(TWI)
baro = SPL06(TWI)


oled = OLED1306(TWI)
oled.fill(oled.BLACK)
oled.show()
sleep_ms(1000)


def show_shape(x_pos, y_pos, shape):
    yp = y_pos
    
    for i in shape:
        xp = x_pos
        for bit_value in i:
            oled.pixel(xp, yp, bit_value)
            xp += 1
            
        yp += 1


while(True):
    AHT25_RH, AHT25_T, AHT25_status, AHT25_CRC = rht.read_sensor()
    SPL06_T = baro.get_tmp()
    SPL06_P = baro.get_prs()
    
    T_avg = ((AHT25_T + SPL06_T) / 2.0)
    
    oled.fill(oled.BLACK)
    oled.text("Weather Station", 2, 2)
    show_shape(2, 20, shape_1)
    show_shape(2, 36, shape_2)
    show_shape(2, 52, shape_3)    
    
    oled.text("Tmp/'C: ", 14, 20)
    oled.text("R.H./%: ", 14, 36)
    oled.text("P/mBar: ", 14, 52)
    
    oled.text(str("%2.2f" %T_avg), 70, 20)
    oled.text(str("%2.2f" %AHT25_RH), 70, 36)
    oled.text(str("%2.2f" %SPL06_P), 70, 52)
    
    oled.show()
    
    print("T.A/'C: " + str("%2.2f" %AHT25_T))
    print("T.S/'C: " + str("%2.2f" %SPL06_T))
    print("R.H./%: " + str("%2.2f" %AHT25_RH))
    print("P/mBar: " + str("%2.2f" %SPL06_P))
    print(" ")
    
    led.toggle()    
    sleep_ms(1000)

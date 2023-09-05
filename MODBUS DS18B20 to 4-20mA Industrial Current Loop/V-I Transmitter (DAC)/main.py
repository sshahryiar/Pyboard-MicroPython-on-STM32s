from pyb import UART, DAC, Pin
from machine import I2C
from utime import sleep_ms
from RGB_LCD import RGB_LCD
from MODBUS_DS18B20 import MODBUS_DS18B20


TWI = I2C(1, freq = 400000)
dac = DAC(1, bits = 12)
uart = UART(6, 9600, bits = 8, parity = None, stop = 1)

lcd = RGB_LCD(TWI)
temp = MODBUS_DS18B20(uart)


def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min) / (x_max - x_min)) * (v - x_min)))


while(True):
    t = temp.get_temp()
    dac_value = map_value(t, 0, 100, 0, 4095)
    dac.write(dac_value)
    
    if((t >= 0) and (t <= 100)):
        t_str = "T/deg C: " + str("%3.1f" %t)
    else:
        t_str = "T/deg C: ---"
        
    lcd.goto_xy(0, 0)
    lcd.put_str("T/'C: " + str("%3.1f  " %t))
    
    lcd.goto_xy(0, 1)
    lcd.put_str("DAC: " + str("%4u  " %dac_value))
    
    print(t_str)
    sleep_ms(400)
    
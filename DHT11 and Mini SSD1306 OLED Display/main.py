from pyb import Pin, LED
from machine import I2C
from SSD1306_mini import OLED96
from utime import sleep_ms
import dht


i2c = I2C(1, freq = 400000)
oled = OLED96(i2c)
led = LED(4)

RH_T = dht.DHT11(Pin('Y10', Pin.IN))


while(True):
    RH_T.measure()
    t = RH_T.temperature()
    rh = RH_T.humidity()
    oled.fill(oled.BLACK)
    oled.text("Pyboard DHT11", 15, 1)
    oled.text("Tc/'C: " + str("%2.1f" %t), 1, 14)
    oled.text("R.H/%: " + str("%2.1f" %rh), 1, 24)
    oled.show()
    led.toggle()
    sleep_ms(400)
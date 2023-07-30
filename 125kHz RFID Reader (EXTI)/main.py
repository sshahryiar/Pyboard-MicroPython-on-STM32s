from pyb import LED, Pin, ExtInt
from machine import I2C
from SSD1306_I2C import OLED1306
from utime import sleep_ms


raw_card_data = 0
count = 30


led = LED(1)


TWI = I2C(scl = 'PB9', sda = 'PB8', freq = 400000)


oled = OLED1306(TWI)
oled.fill(oled.BLACK)
oled.show()


def D0_EXTI_handler(pin):
    global raw_card_data, count
    
    led.off()
    raw_card_data <<= 1
    count += 1

    
ext_d0 = ExtInt(Pin('PA0'), ExtInt.IRQ_FALLING, Pin.PULL_UP, callback = D0_EXTI_handler)


def D1_EXTI_handler(pin):
    global raw_card_data, count

    led.on()
    raw_card_data <<= 1
    raw_card_data |= 1
    count += 1
    
    
ext_d1 = ExtInt(Pin('PA1'), ExtInt.IRQ_FALLING, Pin.PULL_UP, callback = D1_EXTI_handler)


while(True):
    if(count >= 25):
        led.on()
        card_number = (raw_card_data & 0xFFFF)
        facility_code = (0xFF & (raw_card_data >> 0x10))
        oled.fill(oled.BLACK)
        oled.text("PYB RFID Reader", 1, 4, oled.WHITE)
        oled.text("Facility Code:", 1, 20, oled.WHITE)
        oled.text(str("%04u" %facility_code), 1, 30, oled.WHITE)
        oled.text("Serial Number:", 1, 40, oled.WHITE)
        oled.text(str("%04u" %card_number), 1, 50, oled.WHITE)
        oled.show()
        raw_card_data = 0
        count = 0
        sleep_ms(400)
        led.off()

    
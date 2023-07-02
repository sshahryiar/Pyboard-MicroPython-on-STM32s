from pyb import UART, LED
from machine import I2C
from ST7735R import TFT_18
from WiFi import wifi
from AHT20 import AHT20
from BMP280 import BMP280
from utime import sleep_ms
import WiFi_Credentials
import time


sync_hour = 1

i = 0
time_fetch_flag = False
time_sync_status = False
connection_status = False

hour = 10
minute = 10
second = 30
date = 1
month = 1
year = 1970
weekday = 0
yearday = 1
t_avg = 0
bmp_t = 0
bmp_p = 0
aht_t = 0
aht_rh = 0
aht_crc = 0
aht_status = 0

url = 'palamoa.de/json/palamoa_key'


led1 = LED(1)
led2 = LED(2)
led3 = LED(3)
led4 = LED(4)
i2c = I2C(1, freq = 400000)
uart = UART(6, 115200, bits = 8, parity = None, stop = 1, timeout = 1000, rxbuf = 2048)


net = wifi(uart)
tft = TFT_18()
pt = BMP280(i2c)
rht = AHT20(i2c)


while(True):
    bmp_t = pt.get_temperature()
    bmp_p = pt.get_pressure()
    aht_rh, aht_t, aht_status, aht_crc = rht.read_sensor()    
    t_avg = ((bmp_t + aht_t) / 2.0)
   
    if(((minute % 10) == 0) and (second == 30)):
        if(net.get_connection_status() == False):
            net.set_mode(net.STA_AP_mode)
            net.set_SSID_password(WiFi_Credentials.SSID, WiFi_Credentials.password, True)
            print(net.get_IP())
            connection_status = False
            led3.off()
        else:
            led3.on()
            connection_status = True
        
    if(connection_status == True):        
        container_1 = '\r\n' + "{" + "\"P" + "\"" + ":" + "{" + "\"value" + "\"" + ":" + "\"" + str("%3.1f" %bmp_p) + "\"" + "}" + ", "
        container_2 = "\"RH" + "\"" + ":" + "{" + "\"value" + "\"" + ":" + "\"" + str("%3.1f" %aht_rh) + "\"" + "}" + ", "
        container_3 = "\"T" + "\"" + ":" + "{" + "\"value" + "\"" + ":" + "\"" + str("%3.1f" %t_avg) + "\"" + "}" + ", "
        container_4 = "\"device_name" + "\"" + ":" + "\"microarena" + "\"" + "}"
        container = container_1 + container_2 +container_3 + container_4
        
        net.http_post(url, content = container, content_info = "Content-Length: " )
        net.close_connection()
        led4.toggle()
        
        if(time_sync_status == False):            
            if(second == 30):
                time_fetch_flag = True
                time_sync_status = True
        else:     
            if(((hour % sync_hour) == 0) and (minute == 0) and (second == 0)):
                time_fetch_flag = True
                
        if(time_fetch_flag == True):
            led2.on()
            j = net.http_get("worldtimeapi.org/api/timezone/Asia/Dhaka")

            try:
                msg = net.search('unixtime', ',', 1)
                i = int(msg)
                print(i)
                time.gmtime(i)
                year, month, date, hour, minute, second, weekday, yearday = time.localtime() 
                time_fetch_flag = False
                
            except:
                print("Error Syncing Time! Retrying....")
                time_sync_status = False
            
            net.close_connection()
            led2.off()
            
    year, month, date, hour, minute, second, weekday, yearday = time.localtime()

    print("Time: " + str("%02u" % hour) + ":" + str("%02u" % minute) + ":" + str("%02u" % second))
    print("Date: " + str("%02u" % date) + "." + str("%02u" % month) + "." + str("%04u" % year) + "\r\n")
  
    tft.fill(tft.BLACK)
    tft.text("PYB Weather Station", 4, 6, tft.WHITE)
    tft.text("palamoa.de", 40, 16, tft.WHITE)
    tft.text("Tav/'C: " + str("%3.1f" %t_avg), 4, 36, tft.CYAN)
    tft.text("R.H./%: " + str("%3.1f" %aht_rh), 4, 50, tft.YELLOW)
    tft.text("P/mBar: " + str("%3.1f" %bmp_p), 4, 64, tft.GREEN)
    tft.text("Update Interval", 26, 82, tft.BLUE)
    tft.text("Time: " + str("%02u" % hour) + ":" + str("%02u" % minute) + ":" + str("%02u" % second), 4, 96, tft.MAGENTA)
    tft.text("Date: " + str("%02u" % date) + "." + str("%02u" % month) + "." + str("%04u" % year), 4, 110, tft.MAGENTA)
    tft.show()
    
    led1.on()
    sleep_ms(450)
    led1.off()
    sleep_ms(450)

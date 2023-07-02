from pyb import UART, LED
from ST7735R import TFT_18
from WiFi import wifi
from utime import sleep_ms
import WiFi_Credentials
import time
import math


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

url = "worldtimeapi.org/api/timezone/Asia/Dhaka"


led1 = LED(1)
led2 = LED(2)
led3 = LED(3)
led4 = LED(4)
uart = UART(6, 115200, bits = 8, parity = None, stop = 1, timeout = 1000, rxbuf = 2048)


tft = TFT_18()
tft.fill(tft.BLACK)
tft.show()

net = wifi(uart)


def analog_clock(value1, value2, value3):
    tft.ellipse(80, 64, 34, 34, tft.YELLOW)
    tft.ellipse(80, 64, 30, 30, tft.YELLOW)
    
    tft.text("Pyboard Web RTCC", 15, 10, tft.WHITE)
    
    tft.line(80, 64, (80 + int(15 * math.sin(value1 * 5 * 0.105))), int(64 - (15 * math.cos(value1 * 5 * 0.105))), tft.RED)
    tft.line(80, 64, (80 + int(20 * math.sin(value2 * 0.105))), int(64 - (20 * math.cos(value2 * 0.105))), tft.CYAN)
    tft.line(80, 64, (80 + int(25 * math.sin(value3 * 0.105))), int(64 - (25 * math.cos(value3 * 0.105))), tft.GREEN)


while(True):
    tft.fill(tft.BLACK)
    
    if(((minute % 10) == 0) and (second == 30)):
        if(net.get_connection_status() == False):
            net.set_mode(net.STA_AP_mode)
            net.set_SSID_password(WiFi_Credentials.SSID, WiFi_Credentials.password, True)
            print(net.get_IP())
            connection_status = False
            tft.text("-X-", 1, 90, tft.RED)
            led3.off()
        else:
            led3.on()
            tft.text("-*-", 1, 90, tft.RED)
            connection_status = True
        
    if(connection_status == True):        
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
            j = net.http_get(url)

            try:
                msg = net.search('unixtime', ',', 1)
                i = int(msg)
                print(i)
                time.gmtime(i)
                year, month, date, hour, minute, second, weekday, yearday = time.localtime()
                tft.text("Synced", 115, 90, tft.RED)
                time_fetch_flag = False
                
            except:
                print("Error Syncing Time! Retrying....")
                tft.text("Error!", 115, 90, tft.RED)
                time_sync_status = False
            
            net.close_connection()
            led2.off()
            
    year, month, date, hour, minute, second, weekday, yearday = time.localtime()
    
    string_1 = "Time: " + str("%02u" % hour) + ":" + str("%02u" % minute) + ":" + str("%02u" % second)
    string_2 = "Date: " + str("%02u" % date) + "." + str("%02u" % month) + "." + str("%04u" % year) 

    print(string_1)
    print(string_2)
  
    tft.text(string_1, 4, 110, tft.MAGENTA)
    tft.text(string_2, 4, 120, tft.MAGENTA)
    analog_clock(hour, minute, second)

    tft.show()
    
    led1.on()
    sleep_ms(450)
    led1.off()
    sleep_ms(450)
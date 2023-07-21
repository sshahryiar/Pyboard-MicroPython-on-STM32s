from pyb import Pin, RTC, UART
from machine import I2C
from utime import sleep_ms
from WiFi import wifi
from unix_time import unix
from SSD1306_I2C import OLED1306
import math
import WiFi_Credentials
import gc


sync_hour = 1

i = 0
time_fetch_flag = False
time_sync_status = False
connection_status = False

year = 2000
month = 1
date = 1
day = 0
hour = 0
minute = 0
second = 0
tz = +6


LED = Pin("PA1", Pin.OUT)

rtc = RTC()
rtc.datetime((year, month, date, day, hour, minute, second, 0))

td = unix(tz)

soft_I2C = I2C(scl = 'PB15', sda = 'PB13', freq = 100000)

uart = UART(2, 115200, bits = 8, parity = None, stop = 1, timeout = 1000, rxbuf = 2048)

oled = OLED1306(soft_I2C)
oled.fill(oled.BLACK)
oled.show()

net = wifi(uart)


url = 'api.open-notify.org/iss-now.json'


def circle(x, y, r, c):
    oled.hline((x - r), y, (r << 1), c)
    for i in range(1, r):
        a = int(math.sqrt((r * r)-(i * i))) 
        oled.hline((x - a), (y + i), (a << 1), c)
        oled.hline((x - a), (y - i), (a << 1), c)


def analog_clock():
    global hour, minute, second
    
    oled.rect(0, 0, 63, 63, oled.WHITE)
    oled.rect(2, 2, 59, 59, oled.WHITE)
    circle(31, 31, 3, oled.WHITE)        
    oled.line(31, 31, (31 + int(16 * math.sin(hour * 5 * 0.105))), int(31 - (16 * math.cos(hour * 5 * 0.105))), oled.WHITE)
    oled.line(31, 31, (31 + int(20 * math.sin(minute * 0.105))), int(31 - (20 * math.cos(minute * 0.105))), oled.WHITE)
    oled.line(31, 31, (31 + int(25 * math.sin(second * 0.105))), int(31 - (25 * math.cos(second * 0.105))), oled.WHITE)
    
    
def digital_clock():
    global hour, minute, second, year, month, date, day
    
    oled.text("PYB RTCC", 64, 2, oled.WHITE)
    
    oled.text(str("%02u:" %hour), 64, 14, oled.WHITE)
    oled.text(str("%02u:" %minute), 88, 14, oled.WHITE)
    oled.text(str("%02u" %second), 112, 14, oled.WHITE)
    
    oled.text(str("%02u/" %date), 75, 24, oled.WHITE)
    oled.text(str("%02u" %month), 99, 24, oled.WHITE)
    oled.text(str("%02u" %year), 77, 34, oled.WHITE)
    
    
def connection_status_check():
    global minute, second, connection_status
    
    if((((minute % 30) == 0) and (second == 15)) or (connection_status == False)):
        if(net.get_connection_status() == False):
            net.set_mode(net.STA_AP_mode)
            net.set_SSID_password(WiFi_Credentials.SSID, WiFi_Credentials.password, False)
            print(net.get_IP())
            connection_status = False
            gc.collect()
        
        else:
            connection_status = True
        
        
def fetch_time():
    global connection_status, time_fetch_flag, time_sync_status
    global year, month, date, day, hour, minute, second, tz, url
    
    if(connection_status == True):
        oled.text("Comm.Ok", 64, 55, oled.WHITE)
        
        if(time_sync_status == False):
            if(second == 30):
                time_fetch_flag = True
                                
        else:
            if(((hour % sync_hour) == 0) and (minute == 0) and (second == 0)):
                time_fetch_flag = True
                
        if(time_fetch_flag == True):
            gc.collect()
            response = net.http_get(url, echo = False) 
                        
            try:
                print(net.rxd)
                msg = net.search("timestamp", ",", 1, 0)
                i = int(msg)
                print(i)
                year, month, date, hour, minute, second = td.unix_to_date_time(i)
                rtc.datetime((year, month, date, day, hour, minute, second, 0))
                oled.text("Synced", 64, 45, oled.WHITE)
                time_sync_status = True
                
            except:
                oled.text("Error!", 64, 45, oled.WHITE)
                time_sync_status = False
                
            net.close_connection()    
            time_fetch_flag = False
            gc.collect()
                            
    else:
        oled.text("No WiFi!", 64, 55, oled.WHITE)
        

while(True):
    oled.fill(oled.BLACK) 
    
    connection_status_check()
    fetch_time()
    
    string_1 = "Time: " + str("%02u" % hour) + ":" + str("%02u" % minute) + ":" + str("%02u" % second)
    string_2 = "Date: " + str("%02u" % date) + "." + str("%02u" % month) + "." + str("%04u" % year) 

    print(string_1)
    print(string_2)
    
    year, month, date, day, hour, minute, second, tz = rtc.datetime()
    analog_clock()
    digital_clock()
    oled.show()
    LED.high()
    sleep_ms(450)
    LED.low()
    sleep_ms(450)

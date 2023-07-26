from pyb import Pin, RTC, UART
from machine import I2C
from utime import sleep_ms
from WiFi import wifi
from unix_time import unix
from SSD1306_I2C import OLED1306
import WiFi_Credentials
import Open_Weather_Map_Credentials
import gc


sync_hour = 1

i = 0
time_fetch_flag = False
time_sync_status = False
connection_status = False

t = 0
p = 0
rh = 0

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

url_1 = "api.open-notify.org/iss-now.json"
url_2 = 'api.openweathermap.org/data/2.5/weather?q=' + Open_Weather_Map_Credentials.city + ',%20' + Open_Weather_Map_Credentials.country + '&APPID=' + Open_Weather_Map_Credentials.api_key + '&units=metric'
  
    
def display():
    global hour, minute, second, year, month, date, day, t, p, rh
    
    oled.text("Open Weather Map", 1 , 2, oled.WHITE)
    
    oled.text(str("%02u:" %hour), 1, 16, oled.WHITE)
    oled.text(str("%02u:" %minute), 25, 16, oled.WHITE)
    oled.text(str("%02u" %second), 49, 16, oled.WHITE)
    
    oled.text(str("%02u/" %date), 75, 16, oled.WHITE)
    oled.text(str("%02u" %month), 99, 16, oled.WHITE)
    
    oled.text("T./'C: " + str("%2.1f" %t), 1, 26, oled.WHITE)
    oled.text("R.H/%: " + str("%2.1f" %rh), 1, 36, oled.WHITE)
    oled.text("p/kPa: " + str("%3.1f" %p), 1, 46, oled.WHITE)
    
    
    
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
            
            
def fetch_weather():
    global t, p, rh, time_sync_status
    try:
        msg = net.search("temp", ",", 1, 0)
        t = float(msg)
        
        msg = net.search("humidity", "}", 1, 0)
        rh = float(msg)
        
        msg = net.search("pressure", ",", 1, 0)
        p = float(msg)
        
        time_sync_status = True
                        
    except:
        print("Error Fetching Weather Data!")
        
        
def fetch_time():
    global connection_status, time_fetch_flag, tz
    global year, month, date, day, hour, minute, second, url_1, url_2
    
    if(connection_status == True):
        oled.text("WiFi Connected.", 1, 56, oled.WHITE)
        
        if(time_sync_status == False):
            if(second == 30):
                time_fetch_flag = True
                                
        else:
            if(((hour % sync_hour) == 0) and (minute == 0) and (second == 0)):
                time_fetch_flag = True
                
        if(time_fetch_flag == True):
            gc.collect()
            response = net.http_get(url_1, echo = False) 
                        
            try:
                msg = net.search("timestamp", ",", 1, 0)
                i = int(msg)
                
                year, month, date, hour, minute, second = td.unix_to_date_time(i)
                rtc.datetime((year, month, date, day, hour, minute, second, 0))
                net.close_connection()   
                
                gc.collect()
                response = net.http_get(url_2, echo = False)
                sleep_ms(1000)
                                                
                fetch_weather()
                
                net.close_connection()
                
            except:
                time_sync_status = False
                
            net.close_connection()    
            time_fetch_flag = False
            gc.collect()
                            
    else:
        oled.text("No WiFi!     ", 1, 56, oled.WHITE)
        

while(True):
    oled.fill(oled.BLACK) 
    
    connection_status_check()
    fetch_time()
    
    string_1 = "Time: " + str("%02u" % hour) + ":" + str("%02u" % minute) + ":" + str("%02u" % second)
    string_2 = "Date: " + str("%02u" % date) + "." + str("%02u" % month) + "." + str("%04u" % year) 

    print(string_1)
    print(string_2)
    
    year, month, date, day, hour, minute, second, tz = rtc.datetime()
    display()
    oled.show()
    LED.high()
    sleep_ms(450)
    LED.low()
    sleep_ms(450)


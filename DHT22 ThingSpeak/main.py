from pyb import Pin, RTC, UART
from machine import I2C
from utime import sleep_ms
from WiFi import wifi
from unix_time import unix
from SSD1306_I2C import OLED1306
import WiFi_Credentials
import ThingSpeak_Credential
import dht
import gc


sync_hour = 1

i = 0
time_fetch_flag = False
time_sync_status = False
connection_status = False

t = 0
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
dht_pin = Pin('PD1', Pin.IN)

RH_T = dht.DHT22(dht_pin)

rtc = RTC()
rtc.datetime((year, month, date, day, hour, minute, second, 0))

td = unix(tz)

soft_I2C = I2C(scl = 'PB15', sda = 'PB13', freq = 100000)

uart = UART(2, 115200, bits = 8, parity = None, stop = 1, timeout = 1000, rxbuf = 2048)

oled = OLED1306(soft_I2C)
oled.fill(oled.BLACK)
oled.show()

net = wifi(uart)

 
    
def display():
    global hour, minute, second, year, month, date, day, t, p, rh
    
    oled.text("PYB ThingSpeak", 8, 2, oled.WHITE)
    
    oled.text(str("%02u:" %hour), 1, 16, oled.WHITE)
    oled.text(str("%02u:" %minute), 25, 16, oled.WHITE)
    oled.text(str("%02u" %second), 49, 16, oled.WHITE)
    
    oled.text(str("%02u/" %date), 75, 16, oled.WHITE)
    oled.text(str("%02u" %month), 99, 16, oled.WHITE)
    
    oled.text("T./'C: " + str("%2.1f" %t), 1, 30, oled.WHITE)
    oled.text("R.H/%: " + str("%2.1f" %rh), 1, 40, oled.WHITE)
    
    
    
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
            
            
def post_data():
    global t, rh, time_sync_status, second
    
    ts_url = 'api.thingspeak.com/update?api_key=' + ThingSpeak_Credential.api_key + '&field1=' + str(rh) + '&field2=' + str(t)
    
    if((second == 0) and (time_sync_status == True) and (connection_status == True)):  
        gc.collect()
        try:
            response = net.http_get(ts_url, echo = False)
            sleep_ms(100)        
            net.close_connection()
            
        except:
            print("Error Posting Data!")
        
        
def fetch_time():
    global year, month, date, day, hour, minute, second, tz
    global connection_status, time_fetch_flag, time_sync_status
        
    iss_url = "api.open-notify.org/iss-now.json"
    
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
            response = net.http_get(iss_url, echo = False) 
                        
            try:
                msg = net.search("timestamp", ",", 1, 0)
                i = int(msg)
                
                year, month, date, hour, minute, second = td.unix_to_date_time(i)
                rtc.datetime((year, month, date, day, hour, minute, second, 0))
                time_sync_status = True
                net.close_connection()
                
            except:
                time_sync_status = False
                print("Error Fetching Unix Timestamp!")
                
            net.close_connection()    
            time_fetch_flag = False
            gc.collect()
                            
    else:
        oled.text("No WiFi!     ", 1, 56, oled.WHITE)
        

while(True):
    gc.collect()
    RH_T.measure()
    t = RH_T.temperature()
    rh = RH_T.humidity()    
    
    oled.fill(oled.BLACK) 
    
    connection_status_check()
    fetch_time()
    post_data()
    
    year, month, date, day, hour, minute, second, tz = rtc.datetime()
    
    string_1 = "Time: " + str("%02u" % hour) + ":" + str("%02u" % minute) + ":" + str("%02u" % second)
    string_2 = "Date: " + str("%02u" % date) + "." + str("%02u" % month) + "." + str("%04u" % year) 

    print(string_1)
    print(string_2)
    
    display()
    oled.show()
    gc.collect()
    LED.high()
    sleep_ms(400)
    LED.low()
    sleep_ms(400)

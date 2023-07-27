from machine import Pin, I2C
from AHT20 import AHT20
from BMP280 import BMP280
from ST7789V import TFT114
from utime import sleep_ms
import math


i2c = I2C(1, freq = 400000)

tft = TFT114()
pt = BMP280(i2c)
rht = AHT20(i2c)


t_avg = 0
bmp_t = 0
bmp_p = 0
aht_t = 0
aht_rh = 0
aht_crc = 0
aht_status = 0
screen_counter = 0


def screen_1_graphics(value):
    tft.fill(tft.BLACK)
    write_text("Temperature", 36, 1, 2, tft.CYAN)
 
    tft.ellipse(27, 107, 11, 11, tft.WHITE)
    tft.hline(24, 18, 6, tft.WHITE)
    tft.vline(23, 19, 77, tft.WHITE)
    tft.vline(31, 19, 77, tft.WHITE)
    tft.pixel(24, 19, tft.WHITE)
    tft.pixel(30, 19, tft.WHITE)
    tft.ellipse(27, 107, 10, 10, tft.RED, True)
    
    for i in range (28, 100, 7):
        tft.hline(43, i, 10, tft.WHITE)
   
    for i in range (31, 97, 7):
        tft.hline(43, i, 5, tft.WHITE)
        
    tft.text("0'C", 60, 96, tft.WHITE)
    tft.text("50'C", 60, 60, tft.WHITE)
    tft.text("100'C", 60, 28, tft.WHITE)
    
    bar = map_value(value, 0, 100, 0, 75)

    tft.rect(25, (97 - bar), 4, bar, tft.RED, True)
    
    write_text("T/'C", 125, 46, 2, tft.RED)
    write_text(str("%3.1f" %value), 125, 76, 2, tft.RED)
    
    tft.show()
    
    
def screen_2_graphics(value):
    tft.fill(tft.BLACK)
    write_text("R. Humidity", 30, 1, 2, tft.BLUE)
    tft.ellipse(60, 80, 44, 44, tft.WHITE)
    tft.ellipse(60, 80, 40, 40, tft.WHITE)
    
    dial = constrain(value, 0, 100)
    line = map_value(dial, 0, 100, -2.618, 2.618)    
    tft.line(60, 80, (60 + int(36 * math.sin(line))), int(80 - (36 * math.cos(line))), tft.YELLOW)
    tft.line(60, 80, (60 - int(10 * math.sin(line))), int(80 + (10 * math.cos(line))), tft.YELLOW)
    tft.ellipse(60, 80, 3, 3, tft.YELLOW, True)
    
    tft.text("0%", 4, 100, tft.WHITE)
    tft.text("50%", 50, 24, tft.WHITE)
    tft.text("100%", 106, 100, tft.WHITE)
    
    write_text("R.H/%", 145, 46, 2, tft.GREEN)
    write_text(str("%3.1f" %value), 150, 76, 2, tft.GREEN)
    tft.show()
    
    
def screen_3_graphics(value):
    tft.fill(tft.BLACK)
    write_text("Air Pressure", 24, 1, 2, tft.YELLOW)
     
    tft.rect(8, 99, 232, 24, tft.WHITE)
    
    tft.fill_rect(10, 101, 56, 20, tft.CYAN)
    tft.fill_rect(67, 101, 56, 20, tft.GREEN)
    tft.fill_rect(124, 101, 56, 20, tft.YELLOW)
    tft.fill_rect(181, 101, 56, 20, tft.RED)
    
    tft.text("300", 24, 108, tft.BLACK)
    tft.text("600", 81, 108, tft.BLACK)
    tft.text("900", 138, 108, tft.BLACK)
    tft.text("1100", 194, 108, tft.BLACK)
    
    temp = constrain(value, 300, 1200)
    temp = int(map_value(temp, 300, 1200, 10, 230))
    tft.line(temp, 95, (temp - 4), 90, tft.WHITE)
    tft.line(temp, 95, (temp + 4), 90, tft.WHITE)
    tft.line((temp - 4), 90, (temp + 4), 90, tft.WHITE)
    
    write_text("P/mBar", 84, 36, 2, tft.MAGENTA)
    write_text(str("%3.1f" %value), 84, 66, 2, tft.MAGENTA)
   
    tft.show()
    
    
def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min)/(x_max - x_min)) * (v - x_min)))


def constrain(value, min_value, max_value):
    if(value > max_value):
        return max_value
    
    elif(value < min_value):
        return min_value
    
    else:
        return value
        

def write_text(text, x, y, size, color):
        background = tft.pixel(x, y)
        info = []
        
        tft.text(text, x, y, color)
        for i in range(x, x + (8 * len(text))):
            for j in range(y, y + 8):
                px_color = tft.pixel(i, j)
                info.append((i, j, px_color)) if px_color == color else None
        
        tft.text(text, x, y, background)
       
        for px_info in info:
            tft.fill_rect(size*px_info[0] - (size-1)*x , size*px_info[1] - (size-1)*y, size, size, px_info[2]) 


while(True):
    t_avg = ((bmp_t + aht_t) / 2.0)
    
    if(screen_counter == 1):
        screen_2_graphics(aht_rh)
        
    elif(screen_counter == 2):
        screen_3_graphics(bmp_p)
    
    else:
        screen_1_graphics(t_avg)
    
    screen_counter += 1
    
    if(screen_counter >= 3):
        bmp_t = pt.get_temperature()
        bmp_p = pt.get_pressure()
        aht_rh, aht_t, aht_status, aht_crc = rht.read_sensor()
        screen_counter = 0
        
    sleep_ms(2000)

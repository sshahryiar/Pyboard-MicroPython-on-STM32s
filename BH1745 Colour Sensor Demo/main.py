from pyb import LED
from ST7735 import TFT_7735
from BH1745 import BH1745
from utime import sleep_ms


tft = TFT_7735()
bh1745 = BH1745()


def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min)/(x_max - x_min)) * (v - x_min)))


while True:
    R, G, B, C, RGB = bh1745.read_RGBC()
    
    tft.fill(tft.BLACK)
    tft.text("BH1745 Colour Sensor", 1, 6, tft.YELLOW)
    
    r = map_value(R, 0, 255, 1, 85)
    g = map_value(G, 0, 255, 1, 85)
    b = map_value(B, 0, 255, 1, 85)
    c = map_value(C, 0, 255, 1, 85)
    
    tft.fill_rect(70, 26, r, 6, tft.RED)
    tft.fill_rect(70, 36, g, 6, tft.GREEN)
    tft.fill_rect(70, 46, g, 6, tft.BLUE)
    tft.fill_rect(70, 56, c, 6, tft.WHITE)
    
    R = hex(R)
    G = hex(G)
    B = hex(B)
    C = hex(C)
    RGB = hex(RGB)
    
    tft.text("R: " + str(R), 1, 26, tft.RED)
    tft.text("G: " + str(G), 1, 36, tft.GREEN)
    tft.text("B: " + str(B), 1, 46, tft.BLUE)
    tft.text("C: " + str(C), 1, 56, tft.WHITE)
    tft.text("RGB: " + str(RGB), 1, 70, tft.CYAN)
    tft.show()
    
    sleep_ms(900)

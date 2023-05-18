from pyb import LED
from MCP9808 import MCP9808
from ST7789 import TFT_7789
from utime import sleep_ms


tft = TFT_7789()

mcp = MCP9808()


def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min)/(x_max - x_min)) * (v - x_min)))


def draw_background_graphics():
    tft.fill(tft.BLACK)
    tft.print_str(18, 10, 2, tft.WHITE, tft.BLACK, "MCP9808 & PyBoard")
 
    tft.draw_circle(27, 213, 20, False, tft.WHITE)
    tft.draw_H_line(24, 30, 193, tft.WHITE)
    tft.draw_V_line(23, 192, 42, tft.WHITE)
    tft.draw_V_line(31, 192, 42, tft.WHITE)
    tft.draw_pixel(24, 41, tft.WHITE)
    tft.draw_pixel(30, 41, tft.WHITE)
    tft.draw_H_line(25, 29, 40, tft.WHITE)
    tft.draw_circle(27, 213, 19, True, tft.RED)
    
    for i in range (55, 200, 15):
        tft.draw_H_line(43, 53, i, tft.WHITE)
   
    for i in range (62, 193, 15):
        tft.draw_H_line(43, 48, i, tft.WHITE)
        
    tft.print_str(60, 190, 1, tft.WHITE, tft.BLACK, "0'C")
    tft.print_str(60, 120, 1, tft.WHITE, tft.BLACK, "50'C")
    tft.print_str(60, 50, 1, tft.WHITE, tft.BLACK, "100'C")
    tft.print_str(120, 90, 3, tft.WHITE, tft.BLACK, "T/'C:")
   

draw_background_graphics()


while True:
    
    t, stat = mcp.read_T_and_status()
    bar = map_value(t, 0, 100, 192, 42)
    tft.draw_rectangle(25, 42, 29, bar, True, tft.SQUARE, tft.BLACK, tft.BLACK)
    tft.draw_rectangle(25, 193, 29, bar, True, tft.SQUARE, tft.RED, tft.BLACK)
    tft.print_str(120, 130, 3, tft.WHITE, tft.BLACK, str("%3.1f" %t))
    
    sleep_ms(600)
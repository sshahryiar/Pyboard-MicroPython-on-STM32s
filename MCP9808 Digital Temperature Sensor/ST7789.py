from micropython import const
from pyb import Pin, SPI
from utime import sleep_ms


ST7789_DC_pin = 'X12'
ST7789_RST_pin = 'X11'
ST7789_SCK_pin = 'Y6'
ST7789_MOSI_pin = 'Y8'


ST7789_NOP = const(0x00)
ST7789_SWRESET = const(0x01)
ST7789_RDDID = const(0x04)
ST7789_RDDST = const(0x09)
ST7789_RDDPM = const(0x0A)
ST7789_RDD_MADCTL = const(0x0B)
STT7789_RDD_COLMOD = const(0x0C)
ST7789_RDDIM = const(0x0D)
ST7789_RDDSM = const(0x0E)
ST7789_RDDSDR = const(0x0F)

ST7789_SLPIN = const(0x10)
ST7789_SLPOUT = const(0x11)
ST7789_PTLON = const(0x12)
ST7789_NORON = const(0x13)

ST7789_INVOFF = const(0x20)
ST7789_INVON = const(0x21)
ST7789_GAMSET = const(0x26)
ST7789_DISPOFF = const(0x28)
ST7789_DISPON = const(0x29)
ST7789_CASET = const(0x2A)
ST7789_RASET = const(0x2B)
ST7789_RAMWR = const(0x2C)
ST7789_RAMRD = const(0x2E)

ST7789_PTLAR = const(0x30)
ST7789_VSCRDEF = const(0x33)
ST7789_TEOFF = const(0x34)
ST7789_TEON = const(0x35)
ST7789_MADCTL = const(0x36)
ST7789_VSCRSADD = const(0x37)
ST7789_IDMOFF = const(0x38)
ST7789_IDMON = const(0x39)
ST7789_COLMOD = const(0x3A)
ST7789_RAMWRC = const(0x3C)
ST7789_RAMRDC = const(0x3E)

ST7789_TESCAN = const(0x44)
ST7789_RDTESCAN = const(0x45)

ST7789_WRDISBV = const(0x51)
ST7789_RDDISBV = const(0x52)
ST7789_WRCTRLD = const(0x53)
ST7789_RDCTRLD = const(0x54)
ST7789_WRCACE = const(0x55)
ST7789_RDCABC = const(0x56)
ST7789_WRCABCMB = const(0x5E)
ST7789_RDCABCMB = const(0x5F)

ST7789_RDABCSDR = const(0x68)

ST7789_RAMCTRL = const(0xB0)
ST7789_RGBCTRL = const(0xB1)
ST7789_PORCTRL = const(0xB2)
ST7789_FRCTRL1 = const(0xB3)
ST7789_PARCTRL = const(0xB5)
ST7789_GCTRL = const(0xB7)
ST7789_GTADJ = const(0xB8)
ST7789_DGMEN = const(0xBA)
ST7789_VCOMS = const(0xBB)
ST7789_POWSAVE = const(0xBC)
ST7789_DLPOFFSAVE = const(0xBD)

ST7789_LCMCTRL = const(0xC0)
ST7789_IDSET = const(0xC1)
ST7789_VDVVRHEN = const(0xC2)
ST7789_VRHS = const(0xC3)
ST7789_VDVSET = const(0xC4)
ST7789_VCMOFSET = const(0xC5)
ST7789_FRCTR2 = const(0xC6)
ST7789_CABCCTRL = const(0xC7)
ST7789_REGSEL1 = const(0xC8)
ST7789_REGSEL2 = const(0xCA)
ST7789_PWMFRSEL = const(0xCC)

ST7789_PWCTRL1 = const(0xD0)
ST7789_VAPVANEN = const(0xD2)
ST7789_RDID1 = const(0xDA)
ST7789_RDID2 = const(0xDB)
ST7789_RDID3 = const(0xDC)
ST7789_CMD2EN = const(0xDF)

ST7789_PVGAMCTRL = const(0xE0)
ST7789_NVGAMCTRL = const(0xE1)
ST7789_DGMLUTR = const(0xE2)
ST7789_DGMLUTB = const(0xE3)
ST7789_GATECTRL = const(0xE4)
ST7789_SPI2EN = const(0xE7)
ST7789_PWCTRL2 = const(0xE8)
ST7789_EQCTRL = const(0xE9)
ST7789_PROMCTRL = const(0xEC)

ST7789_PROMEN = const(0xFA)
ST7789_NVMSET = const(0xFC)
ST7789_PROMACT = const(0xFE)

ST7789_TFT_WIDTH = const(240)
ST7789_TFT_HEIGHT = const(240)

CMD = False
DAT = True

LOW = False
HIGH = True


font = [
     [0x00, 0x00, 0x00, 0x00, 0x00] #0x20
    ,[0x00, 0x00, 0x5f, 0x00, 0x00] #0x21 !
    ,[0x00, 0x07, 0x00, 0x07, 0x00] #0x22 "
    ,[0x14, 0x7f, 0x14, 0x7f, 0x14] #0x23 #
    ,[0x24, 0x2a, 0x7f, 0x2a, 0x12] #0x24 $
    ,[0x23, 0x13, 0x08, 0x64, 0x62] #0x25 %
    ,[0x36, 0x49, 0x55, 0x22, 0x50] #0x26 &
    ,[0x00, 0x05, 0x03, 0x00, 0x00] #0x27 '
    ,[0x00, 0x1c, 0x22, 0x41, 0x00] #0x28 (
    ,[0x00, 0x41, 0x22, 0x1c, 0x00] #0x29 )
    ,[0x14, 0x08, 0x3e, 0x08, 0x14] #0x2a *
    ,[0x08, 0x08, 0x3e, 0x08, 0x08] #0x2b +
    ,[0x00, 0x50, 0x30, 0x00, 0x00] #0x2c ,
    ,[0x08, 0x08, 0x08, 0x08, 0x08] #0x2d -
    ,[0x00, 0x60, 0x60, 0x00, 0x00] #0x2e .
    ,[0x20, 0x10, 0x08, 0x04, 0x02] #0x2f /
    ,[0x3e, 0x51, 0x49, 0x45, 0x3e] #0x30 0
    ,[0x00, 0x42, 0x7f, 0x40, 0x00] #0x31 1
    ,[0x42, 0x61, 0x51, 0x49, 0x46] #0x32 2
    ,[0x21, 0x41, 0x45, 0x4b, 0x31] #0x33 3
    ,[0x18, 0x14, 0x12, 0x7f, 0x10] #0x34 4
    ,[0x27, 0x45, 0x45, 0x45, 0x39] #0x35 5
    ,[0x3c, 0x4a, 0x49, 0x49, 0x30] #0x36 6
    ,[0x01, 0x71, 0x09, 0x05, 0x03] #0x37 7
    ,[0x36, 0x49, 0x49, 0x49, 0x36] #0x38 8
    ,[0x06, 0x49, 0x49, 0x29, 0x1e] #0x39 9
    ,[0x00, 0x36, 0x36, 0x00, 0x00] #0x3a :
    ,[0x00, 0x56, 0x36, 0x00, 0x00] #0x3b ;
    ,[0x08, 0x14, 0x22, 0x41, 0x00] #0x3c <
    ,[0x14, 0x14, 0x14, 0x14, 0x14] #0x3d =
    ,[0x00, 0x41, 0x22, 0x14, 0x08] #0x3e >
    ,[0x02, 0x01, 0x51, 0x09, 0x06] #0x3f ?
    ,[0x32, 0x49, 0x79, 0x41, 0x3e] #0x40 @
    ,[0x7e, 0x11, 0x11, 0x11, 0x7e] #0x41 A
    ,[0x7f, 0x49, 0x49, 0x49, 0x36] #0x42 B
    ,[0x3e, 0x41, 0x41, 0x41, 0x22] #0x43 C
    ,[0x7f, 0x41, 0x41, 0x22, 0x1c] #0x44 D
    ,[0x7f, 0x49, 0x49, 0x49, 0x41] #0x45 E
    ,[0x7f, 0x09, 0x09, 0x09, 0x01] #0x46 F
    ,[0x3e, 0x41, 0x49, 0x49, 0x7a] #0x47 G
    ,[0x7f, 0x08, 0x08, 0x08, 0x7f] #0x48 H
    ,[0x00, 0x41, 0x7f, 0x41, 0x00] #0x49 I
    ,[0x20, 0x40, 0x41, 0x3f, 0x01] #0x4a J
    ,[0x7f, 0x08, 0x14, 0x22, 0x41] #0x4b K
    ,[0x7f, 0x40, 0x40, 0x40, 0x40] #0x4c L
    ,[0x7f, 0x02, 0x0c, 0x02, 0x7f] #0x4d M
    ,[0x7f, 0x04, 0x08, 0x10, 0x7f] #0x4e N
    ,[0x3e, 0x41, 0x41, 0x41, 0x3e] #0x4f O
    ,[0x7f, 0x09, 0x09, 0x09, 0x06] #0x50 P
    ,[0x3e, 0x41, 0x51, 0x21, 0x5e] #0x51 Q
    ,[0x7f, 0x09, 0x19, 0x29, 0x46] #0x52 R
    ,[0x46, 0x49, 0x49, 0x49, 0x31] #0x53 S
    ,[0x01, 0x01, 0x7f, 0x01, 0x01] #0x54 T
    ,[0x3f, 0x40, 0x40, 0x40, 0x3f] #0x55 U
    ,[0x1f, 0x20, 0x40, 0x20, 0x1f] #0x56 V
    ,[0x3f, 0x40, 0x38, 0x40, 0x3f] #0x57 W
    ,[0x63, 0x14, 0x08, 0x14, 0x63] #0x58 X
    ,[0x07, 0x08, 0x70, 0x08, 0x07] #0x59 Y
    ,[0x61, 0x51, 0x49, 0x45, 0x43] #0x5a Z
    ,[0x00, 0x7f, 0x41, 0x41, 0x00] #0x5b [
    ,[0x02, 0x04, 0x08, 0x10, 0x20] #0x5c ?
    ,[0x00, 0x41, 0x41, 0x7f, 0x00] #0x5d ]
    ,[0x04, 0x02, 0x01, 0x02, 0x04] #0x5e ^
    ,[0x40, 0x40, 0x40, 0x40, 0x40] #0x5f _
    ,[0x00, 0x01, 0x02, 0x04, 0x00] #0x60 `
    ,[0x20, 0x54, 0x54, 0x54, 0x78] #0x61 a
    ,[0x7f, 0x48, 0x44, 0x44, 0x38] #0x62 b
    ,[0x38, 0x44, 0x44, 0x44, 0x20] #0x63 c
    ,[0x38, 0x44, 0x44, 0x48, 0x7f] #0x64 d
    ,[0x38, 0x54, 0x54, 0x54, 0x18] #0x65 e
    ,[0x08, 0x7e, 0x09, 0x01, 0x02] #0x66 f
    ,[0x0c, 0x52, 0x52, 0x52, 0x3e] #0x67 g
    ,[0x7f, 0x08, 0x04, 0x04, 0x78] #0x68 h
    ,[0x00, 0x44, 0x7d, 0x40, 0x00] #0x69 i
    ,[0x20, 0x40, 0x44, 0x3d, 0x00] #0x6a j
    ,[0x7f, 0x10, 0x28, 0x44, 0x00] #0x6b k
    ,[0x00, 0x41, 0x7f, 0x40, 0x00] #0x6c l
    ,[0x7c, 0x04, 0x18, 0x04, 0x78] #0x6d m
    ,[0x7c, 0x08, 0x04, 0x04, 0x78] #0x6e n
    ,[0x38, 0x44, 0x44, 0x44, 0x38] #0x6f o
    ,[0x7c, 0x14, 0x14, 0x14, 0x08] #0x70 p
    ,[0x08, 0x14, 0x14, 0x18, 0x7c] #0x71 q
    ,[0x7c, 0x08, 0x04, 0x04, 0x08] #0x72 r
    ,[0x48, 0x54, 0x54, 0x54, 0x20] #0x73 s
    ,[0x04, 0x3f, 0x44, 0x40, 0x20] #0x74 t
    ,[0x3c, 0x40, 0x40, 0x20, 0x7c] #0x75 u
    ,[0x1c, 0x20, 0x40, 0x20, 0x1c] #0x76 v
    ,[0x3c, 0x40, 0x30, 0x40, 0x3c] #0x77 w
    ,[0x44, 0x28, 0x10, 0x28, 0x44] #0x78 x
    ,[0x0c, 0x50, 0x50, 0x50, 0x3c] #0x79 y
    ,[0x44, 0x64, 0x54, 0x4c, 0x44] #0x7a z
    ,[0x00, 0x08, 0x36, 0x41, 0x00] #0x7b [
    ,[0x00, 0x00, 0x7f, 0x00, 0x00] #0x7c |
    ,[0x00, 0x41, 0x36, 0x08, 0x00] #0x7d ]
    ,[0x10, 0x08, 0x08, 0x10, 0x08] #0x7e ?
    ,[0x78, 0x46, 0x41, 0x46, 0x78] #0x7f ?
]


class TFT_7789():
    
    def __init__(self):
        self.width = ST7789_TFT_WIDTH
        self.height = ST7789_TFT_HEIGHT
        
        self.NO = False
        self.YES = True
        
        self.OFF = False
        self.ON = True
        
        self.ROUNDED = False
        self.SQUARE = True

        self.BLACK = const(0x0000)
        self.BLUE = const(0x001F)
        self.RED = const(0xF800)
        self.GREEN = const(0x07E0)
        self.CYAN = const(0x07FF)
        self.MAGENTA = const(0xF81F)
        self.YELLOW = const(0x07FF)
        self.WHITE = const(0xFFFF)    

        self.ST7789_RST = Pin(ST7789_RST_pin, Pin.OUT_PP)
        self.ST7789_SCK = Pin(ST7789_SCK_pin, Pin.OUT_PP)
        self.ST7789_MOSI = Pin(ST7789_MOSI_pin, Pin.OUT_PP)

        self.ST7789_SPI = SPI(2, SPI.CONTROLLER, baudrate = 10_000_000, polarity = 1, phase = 1, bits = 8, firstbit = SPI.MSB)
        
        self.ST7789_DC = Pin(ST7789_DC_pin, Pin.OUT_PP)
        
        self.TFT_init()
        
        
    def disp_reset(self):
        self.ST7789_RST.value(HIGH)
        sleep_ms(60)
        self.ST7789_RST.value(LOW)
        sleep_ms(60)
        self.ST7789_RST.value(HIGH)
        sleep_ms(60)
        

    def send(self, value, mode):
        self.ST7789_DC.value(mode)
        self.ST7789_SPI.send(bytearray([value]))
        
    
    def send_word(self, value):
        self.ST7789_DC.value(DAT)
        self.ST7789_SPI.send(bytearray([((value & 0xFF00) >> 8)]))
        self.ST7789_SPI.send(bytearray([(value & 0x00FF)]))


    def TFT_init(self):
        self.disp_reset()
        
        self.send(ST7789_SWRESET, CMD)
        sleep_ms(40)
        
        self.send(ST7789_SLPOUT, CMD)
        sleep_ms(40)

        self.send(ST7789_COLMOD, CMD)
        self.send(0x55, DAT)
         
        self.send(ST7789_PORCTRL, CMD)
        self.send(0x0C, DAT)
        self.send(0x0C, DAT)
        self.send(0x00, DAT)
        self.send(0x33, DAT)
        self.send(0x33, DAT)

        self.send(ST7789_GCTRL, CMD)
        self.send(0x35, DAT)

        self.send(ST7789_VCOMS, CMD)
        self.send(0x19, DAT)

        self.send(ST7789_LCMCTRL, CMD)
        self.send(0x2C, DAT)

        self.send(ST7789_VDVVRHEN, CMD)
        self.send(0x01, DAT)

        self.send(ST7789_VRHS, CMD)
        self.send(0x12, DAT)

        self.send(ST7789_VDVSET, CMD)
        self.send(0x20, DAT)

        self.send(ST7789_FRCTR2, CMD)
        self.send(0x0F, DAT)

        self.send(ST7789_PWCTRL1, CMD)
        self.send(0xA4, DAT)
        self.send(0xA1, DAT)

        self.send(ST7789_PVGAMCTRL, CMD)
        self.send(0xD0, DAT)
        self.send(0x04, DAT)
        self.send(0x0D, DAT)
        self.send(0x11, DAT)
        self.send(0x13, DAT)
        self.send(0x2B, DAT)
        self.send(0x3F, DAT)
        self.send(0x54, DAT)
        self.send(0x4C, DAT)
        self.send(0x18, DAT)
        self.send(0x0D, DAT)
        self.send(0x0B, DAT)
        self.send(0x1F, DAT)
        self.send(0x23, DAT)

        self.send(ST7789_NVGAMCTRL, CMD)
        self.send(0xD0, DAT)
        self.send(0x04, DAT)
        self.send(0x0C, DAT)
        self.send(0x11, DAT)
        self.send(0x13, DAT)
        self.send(0x2C, DAT)
        self.send(0x3F, DAT)
        self.send(0x44, DAT)
        self.send(0x51, DAT)
        self.send(0x2F, DAT)
        self.send(0x1F, DAT)
        self.send(0x1F, DAT)
        self.send(0x20, DAT)
        self.send(0x23, DAT)
        
        self.send(ST7789_MADCTL, CMD)
        self.send(0x07, DAT) 
        
        self.set_windows(0, 0, ST7789_TFT_WIDTH, ST7789_TFT_HEIGHT)
        
        self.send(ST7789_INVON, CMD)
        self.send(ST7789_NORON, CMD)
        self.send(ST7789_DISPON, CMD)
        sleep_ms(40)
       

    def colour_generator(self, r, g, b):
        r = (r & 0xF8)
        g = ((g & 0xFC) >> 2)
        b = ((b & 0xF8) >> 3)
        
        colour = r
        colour |= (b << 8)
        colour |= ((g & 0x38) >> 3)
        colour |= ((g & 0x07) << 13)
    
        return colour
    
    
    def set_windows(self, xs, ys, xe, ye):
        self.send(ST7789_CASET, CMD)
        self.send_word(xs)
        self.send_word(xe)

        self.send(ST7789_RASET, CMD)
        self.send_word(ys)
        self.send_word(ye)
 
        self.send(ST7789_RAMWR, CMD)


    def set_RAM_address(self):
        self.set_windows(0, 0, (self.width - 1), (self.height - 1)) 
        
    
    def fill(self, colour):
        self.set_RAM_address()
        
        l = self.height
        while(l > 0):
            w = self.width
            while(w > 0):
                self.send_word(colour)
                w -= 1
            
            l -= 1
                
                
    def Swap_Colour(self, colour):
        return ((colour << 0x000B) | (colour & 0x07E0) | (colour >> 0x000B))


    def Color565(self, r, g, b):
        return (((r & 0xF8) << 0x08) | ((g & 0xFC) << 0x03) | (b >> 0x03))


    def draw_pixel(self, x_pos, y_pos, colour):
        self.set_windows(x_pos, y_pos, (x_pos + 1), (y_pos + 1))
        self.send_word(colour)
      
      
    def draw_line(self, x1, y1, x2, y2, colour):
        dx = (x2 - x1)
        dy = (y2 - y1)
        
        if(dy < 0):
            dy = -dy
            step_y = -1
            
        else:
            step_y = 1
            
        if(dx < 0):
            dx = -dx
            step_x = -1
            
        else:
            step_x = 1
            
        dx <<= 1
        dy <<= 1
        
        self.draw_pixel(x1, y1, colour)
        
        if(dx > dy):
            fraction = (dy - (dx >> 1))
            while(x1 != x2):
                if(fraction >= 0):
                    y1 += step_y
                    fraction -= dx
                
                x1 += step_x
                fraction += dy
                
                self.draw_pixel(x1, y1, colour)
                
        else:
            fraction = (dx - (dy >> 1))
            while(y1 != y2):
                if(fraction >= 0):
                    x1 += step_x
                    fraction -= dy
                
                y1 += step_y
                fraction += dx
                
                self.draw_pixel(x1, y1, colour)
             
             
    def draw_V_line(self, x1, y1, y2, colour):
        self.draw_line(x1, y1, x1, y2, colour)
        
        
    def draw_H_line(self, x1, x2, y1, colour):
        self.draw_line(x1, y1, x2, y1, colour)
        
        
    def draw_circle(self, xc, yc, r, f, colour):
       a = 0
       b = r
       p = (1 - b)
       
       while(a <= b):
           if(f == self.YES):
               self.draw_line((xc - a), (yc + b), (xc + a), (yc + b), colour)
               self.draw_line((xc - a), (yc - b), (xc + a), (yc - b), colour)
               self.draw_line((xc - b), (yc + a), (xc + b), (yc + a), colour)
               self.draw_line((xc - b), (yc - a), (xc + b), (yc - a), colour)
               
           else:
               self.draw_pixel((xc + a), (yc + b), colour)
               self.draw_pixel((xc + b), (yc + a), colour)
               self.draw_pixel((xc - a), (yc + b), colour)
               self.draw_pixel((xc - b), (yc + a), colour)
               self.draw_pixel((xc + b), (yc - a), colour)
               self.draw_pixel((xc + a), (yc - b), colour)
               self.draw_pixel((xc - a), (yc - b), colour)
               self.draw_pixel((xc - b), (yc - a), colour)
            
           if(p < 0):
               p += (3 + (2 * a))
               a += 1
            
           else:
               p += (5 + (2 * (a  - b)))
               a += 1
               b -= 1
               
    def draw_triangle(self, x1, y1, x2, y2, x3, y3, f, colour):
        a = 0
        b = 0
        l = 0
        sa = 0
        sb = 0
        yp = 0
        dx12 = 0
        dx23 = 0
        dx13 = 0
        dy12 = 0
        dy23 = 0
        dy13 = 0
        
        if(f == self.YES):
            if(y1 > y2):
                y1, y2 = y2, y1
                x1, x2 = x2, x1
                
            if(y2 > y3):
                y2, y3 = y3, y2
                x2, x3 = x3, x2
                
            if(y3 > y1):
                y1, y3 = y3, y1
                x1, x3 = x3, x1
                
            if(y1 == y3):
                a = x1
                b = a
                
                if(x2 < a):
                    a = x2
                
                elif(x2 > b):
                    b = x2
                    
                if(x3 < a):
                    a = x3
                
                elif(x3 > b):
                    b = x3
                
                self.draw_H_line(a, (a + (b - (a + 1))), y1, colour)
                return
            
            dx12 = (x2 - x1)
            dy12 = (y2 - y1)
            dx13 = (x3 - x1)
            dy13 = (y3 - y1)
            dx23 = (x3 - x2)
            dy23 = (y3 - y2)
            
            if(y2 == y3):
                l = (y2 + 1)
            
            else:
                l = y2
            
            for yp in range(y1, l):
                a = int(float(x1)+ float(sa / dy12))
                b = int(float(x1) + float(sb / dy13))
                
                sa += dx12
                sb += dx13
                
                if(a > b):
                    a, b = b, a
                
                self.draw_H_line(a, (a + (b - (a + 1))), yp, colour)
            
            sa = int(float(dx23) * float(yp - y2))
            sb = int(float(dx13 )* float(yp - y1))

            while(yp <= y3):
                a = int(float(x2) + float(sa / dy23))
                b = int(float(x1) + float(sb / dy13))
                sa += dx23
                sb += dx13

                if(a > b):
                    a, b = b, a
                    
                self.draw_H_line(a, (a + (b - (a + 1))), yp, colour)
                yp += 1
            
        else:
            self.draw_line(x1, y1, x2, y2, colour)
            self.draw_line(x2, y2, x3, y3, colour)
            self.draw_line(x1, y1, x3, y3, colour)
            
    
    def draw_rectangle(self, x1, y1, x2, y2, f, type, colour, back_colour):       
        if(f == self.YES):
            
            if(x1 < x2):
                xmin = x1
                xmax = x2
            
            else:
                xmin = x2
                xmax = x1
                
            if(y1 < y2):
                ymin = y1
                ymax = y2
            
            else:
                ymin = y2
                ymax = y1
                
            while(xmin <= xmax):
                i = ymin
                while(i <= ymax):
                    self.draw_pixel(xmin, i, colour)
                    i += 1
                xmin += 1
                
        else:
            self.draw_V_line(x1, y1, y2, colour)
            self.draw_V_line(x2, y1, y2, colour)
            self.draw_H_line(x1, x2, y1, colour)
            self.draw_H_line(x1, x2, y2, colour)
    
        if(type == self.ROUNDED):
            self.draw_pixel(x1, y1, back_colour)
            self.draw_pixel(x1, y2, back_colour)
            self.draw_pixel(x2, y1, back_colour)
            self.draw_pixel(x2, y2, back_colour)
        
            
    def draw_font_pixel(self, xp, yp, colour, font_size):
        self.set_windows(xp, yp, (xp + font_size - 1), (yp + font_size - 1))
        
        for i in range(0, (font_size * font_size)):
            self.send_word(colour)
            
    
    def print_font(self, x_pos, y_pos, font_size, colour, back_colour, ch):
        if(font_size < 0):
            font_size = 1
        
        if(x_pos < font_size):
            x_pos = font_size
            
        for i in range(0, 5):
            for j in range(0, 8):
                value = 0x00
                value = font[ord(ch) - 0x20][i]
                
                if((value >> j) & 0x01):
                    self.draw_font_pixel(x_pos, y_pos, colour, font_size)
                
                else:
                    self.draw_font_pixel(x_pos, y_pos, back_colour, font_size)
                    
                y_pos = font_size + y_pos
            
            y_pos -= (font_size << 0x03)
            x_pos += font_size
            
        x_pos += font_size
        
        if(x_pos > self.width):
            x_pos = (font_size + 0x01)
            y_pos += (font_size << 0x03)
            
    
    def print_str(self, x_pos, y_pos, font_size, colour, back_colour, ch_str):
        for chr in ch_str:
            self.print_font(x_pos, y_pos, font_size, colour, back_colour, chr)
            x_pos += (font_size * 6)

from pyb import Pin, SPI, ADC
from WS2812 import WS2812
from utime import sleep_ms


dly = 0


colour_matrix = [
    (50, 100, 200), (35, 70, 140), (30, 45, 60), (5, 7, 10),    
    (200, 100, 50), (140, 70, 35), (60, 45, 30), (10, 7, 5),    
    (240, 200, 120), (170, 140, 60), (90, 80, 45), (40, 30, 15),    
    (200, 0, 0), (140, 0, 0), (60, 0, 0), (10, 0, 0),    
    (0, 200, 0), (0, 140, 0), (0, 60, 0), (0, 10, 0),    
    (0, 0, 200), (0, 0, 140), (0, 0, 60), (0, 0, 10),    
    (200, 200, 200), (140, 140, 140), (60, 60, 60), (10, 10, 10),    
    (120, 0, 0), (0, 120, 0), (0, 0, 120), (90, 90, 90),
    ]


adc = ADC(Pin("PA0"))

spi = SPI(2, mode = SPI.MASTER, baudrate = 10_000_000, polarity = 0, phase = 1, bits = 8, firstbit = SPI.MSB)

np = WS2812(8, spi)


while (True):
    for j in range (0, 32, 4):
        for i in range (4, -1, -1):
            np.send(i, colour_matrix[j][0], colour_matrix[j][1], colour_matrix[j][2])
            np.send((i + 1), colour_matrix[j + 1][0], colour_matrix[j + 1][1], colour_matrix[j + 1][2])
            np.send((i + 2), colour_matrix[j + 2][0], colour_matrix[j + 2][1], colour_matrix[j + 2][2])
            np.send((i + 3), colour_matrix[j + 3][0], colour_matrix[j + 3][1], colour_matrix[j + 3][2])
            np.show()
            sleep_ms(dly)
            
        for i in range (4, -1, -1):
            np.send(i, 0, 0, 0)
            np.send((i + 1), 0, 0, 0)
            np.send((i + 2), 0, 0, 0)
            np.send((i + 3), 0, 0, 0)
            np.show()
            sleep_ms(dly)
        
        dly = ((adc.read() + 96) >> 3)



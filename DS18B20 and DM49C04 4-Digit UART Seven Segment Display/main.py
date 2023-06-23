from pyb import UART
from DS18B20 import DS18B20
from utime import sleep_ms


ts = DS18B20('X2')
disp = UART(1, 9600, bits = 8, parity = None, stop = 1)


def show_temp(value):
    disp.writechar(0x23)
    disp.writechar((0x30 + (value // 100)))
    disp.writechar((0x30 + (value % 100) // 10))
    disp.writechar(0x2A)
    disp.writechar((0x30 + (value % 10)))
    disp.writechar(0x43)    


while(True):
    tmp = ts.get_T()
    print("T/'C: " + str("%2.1f" %tmp) + "\r")
    tmps = int(10 * tmp)
    show_temp(tmps)

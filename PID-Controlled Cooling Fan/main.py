from pyb import Pin, SPI, Timer
from SSD1309 import OLED1309
from DS18B20 import DS18B20
from utime import sleep_ms, sleep_us
from micropython import const


points = const(32)

j = 0
k = 0
pv = 0
sv = 35
kp = 4.69
kd = 0.06
ki = 0.09
rpm = 0
pulse = 1
error = 0
integral = 0
derivative  = 0
last_capture = 0
previous_error = 0
pwm_duty_cycle = 0
bar = bytearray(b'\x3F' * points)

cs_pin = Pin('PB7', Pin.OUT_PP) 
dc_pin = Pin('PB8', Pin.OUT_PP) 
rst_pin = Pin('PB9', Pin.OUT_PP)
cap_pin = Pin('PA1', Pin.IN)
pwm_pin = Pin('PB4', Pin.OUT_PP)

spi = SPI(2, mode = SPI.MASTER, baudrate = 1000000, polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB)

oled = OLED1309(spi, dc_pin, rst_pin, cs_pin)

tmp = DS18B20('PA3')


def input_capture(timer):
    global last_capture, pulse
    
    pulse = (in_cap.capture() - last_capture)
    last_capture = in_cap.capture()
    pulse &= 0x0FFFFFFF


TIM2 = Timer(2,
             prescaler = 83,
             period = 0x0FFFFFFF)

in_cap = TIM2.channel(2,
                      mode = Timer.IC,
                      pin = cap_pin,
                      polarity = Timer.RISING,
                      callback = input_capture)


TIM3 = Timer(3,
             mode = Timer.UP,
             prescaler = 20,
             period = 999)

pwm  = TIM3.channel(1,
                    mode = Timer.PWM,
                    pin = pwm_pin)


def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min) / (x_max - x_min)) * (v - x_min)))


def constrain(value, min_value, max_value):
    if(value > max_value):
        return max_value
    
    elif(value < min_value):
        return min_value
    
    else:
        return value


oled.fill(oled.BLACK)
oled.show()


while(True):
    rpm = (15000000 / (pulse + 0.00001))
    rpm = constrain(rpm, 0, 3500)
    pv = tmp.get_T()
    
    error = (pv - sv)
    integral += error
    derivative = (error - previous_error)
    
    integral = constrain(integral, -600, 600)
    
    print("E: " + str("%2.2f" %error)
          + "  I: " + str("%2.2f" %integral)
          + "  D: " + str("%2.2f" %derivative))
    
    pwm_duty_cycle = ((kp * error) + (kd * derivative) + (ki * integral))
    pwm_duty_cycle = constrain(pwm_duty_cycle, 0, 100)

    pwm.pulse_width_percent(pwm_duty_cycle)
    
    bar[j] = map_value(rpm, 0, 3500, 63, 35)
   
    oled.fill(oled.BLACK)
    oled.text("PID Fan Control", 6, 4, oled.WHITE)
    oled.text((str("%4u" %rpm) + " RPM"+ " " + str("%3u" %pwm_duty_cycle) + "%"), 1, 15, oled.WHITE)
    oled.text(("PV: " + str("%2u" %pv) + "  SV: " + str("%2u" %sv)), 1, 25, oled.WHITE)  
    
    for k in range (0, points, 1):
        oled.fill_rect((k * 4), bar[k], 2, (63 - bar[k]), oled.WHITE)
    
    j += 1
    
    if(j >= points):
        j = 0
  
    oled.show()

    previous_error = error
    sleep_ms(200)

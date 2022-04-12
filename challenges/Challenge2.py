
from mpu6050 import MPU6050
import pyb
from pyb import Pin, Timer, ADC
from oled_938 import OLED_938	# Use OLED display driver

# Define pins to control motor
A1 = Pin('X3', Pin.OUT_PP)		# Control direction of motor A
A2 = Pin('X4', Pin.OUT_PP)
PWMA = Pin('X1')				# Control speed of motor A
B1 = Pin('X7', Pin.OUT_PP)		# Control direction of motor B
B2 = Pin('X8', Pin.OUT_PP)
PWMB = Pin('X2')				# Control speed of motor B

# Configure timer 2 to produce 1KHz clock for PWM control
tim = Timer(2, freq = 1000)
motorA = tim.channel (1, Timer.PWM, pin = PWMA)
motorB = tim.channel (2, Timer.PWM, pin = PWMB)

# Define 5k Potentiometer
pot = pyb.ADC(Pin('X11'))

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
i2c = pyb.I2C(2, pyb.I2C.MASTER)
devid = i2c.scan()				# find the I2C device number
oled = OLED_938(
    pinout={"sda": "Y10", "scl": "Y9", "res": "Y8"},
    height=64, external_vcc=False, i2c_devid=i2c.scan()[0],
)
oled.poweron()
oled.init_display()
oled.draw_text(0,0, 'Lab 5 - Task 3b')
oled.display()

imu = MPU6050(1,False)

def A_forward(value):
	A1.low()
	A2.high()
	motorA.pulse_width_percent(value)

def A_back(value):
	A2.low()
	A1.high()
	motorA.pulse_width_percent(value)
	
def A_stop():
	A1.high()
	A2.high()
	
def B_forward(value):
	B2.low()
	B1.high()
	motorB.pulse_width_percent(value)

def B_back(value):
	B1.low()
	B2.high()
	motorB.pulse_width_percent(value)
	
def B_stop():
	B1.high()
	B2.high()

def get_pitch():
    global pitch
    pitch = int(imu.pitch())
    return pitch

def get_roll():
    global roll
    roll = int(imu.roll())
    return roll

while True:

    pitch = get_pitch()
    pitch = max(min(pitch,100),-100)
    roll = get_roll()
    roll = max(min(roll,100),-100)

    if (pitch >= 0):
        A_forward(pitch)
    else:
        A_back(abs(pitch))

    if (roll >= 0):
        B_forward(roll)
    else:
        B_back(abs(roll))

    oled.draw_text(0,10, 'Pitch - motor A:{:5d}'.format(pitch))
    oled.draw_text(0,10, 'Roll - motor B:{:5d}'.format(roll))



#measured speeds without any resistance
real_speed_a_9v = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.02564103, 0.0, 0.0, 0.0, 0.0, 0.1538462, 0.1538462, 0.1794872, 0.2307692, 0.3076923, 0.4102564, 0.4615385, 0.5128205, 0.5897436, 0.6666667, 0.6923077, 0.7692308, 0.7948718, 0.897436, 0.9230769, 1.0, 1.025641, 1.076923, 1.102564, 1.179487, 1.205128, 1.25641, 1.307692, 1.358974, 1.410256, 1.48718, 1.51282, 1.589744, 1.615385, 1.384615, 1.641026, 1.74359, 1.564103, 1.871795, 1.923077, 1.358974, 1.769231, 2.0, 1.948718, 2.179487, 2.205128, 2.179487, 2.230769, 2.358974, 2.410256, 2.435897, 2.51282, 2.538461, 2.589744, 2.615385, 2.205128, 2.74359, 2.77, 2.794872, 2.846154, 2.871795, 2.948718, 2.974359, 3.051282, 3.102564, 3.128205, 3.179487, 3.230769, 3.25641, 3.307692, 3.358974, 3.384615, 3.461539, 3.48718, 3.538461, 3.538461, 3.564103, 3.641026, 3.692308, 3.717949, 3.794872, 3.820513, 3.897436, 3.923077, 3.948718, 3.974359, 4.025641, 4.051282, 4.076923, 4.153846, 4.179487, 4.230769, 4.230769]

from Challenge2 import get_pitch
import pyb
from pyb import Pin, Timer, ADC, LED
from oled_938 import OLED_938
from mpu6050 import MPU6050
from PIDmotor import PIDm

# Define LEDs
b_LED = LED(4)

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

# IMU connected to X9 and X10
imu = MPU6050(1, False)    	# Use I2C port 1 on Pyboard

def read_imu(dt):
	
	global g_pitch
	global g_roll
	alpha = 0.7    # larger = longer time constant
	pitch = int(imu.pitch())
	g_pitch = alpha*(g_pitch + imu.get_gy()*dt*0.001) + (1-alpha)*pitch

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
oled.draw_text(0,0, 'Challenge 3')
oled.display()
	
def isr_motorA(self, line):
	countA += 1
			
def isr_motorB(self, line):
	countB += 1

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
	
# Initialise variables
A_speed = 0
A_count = 0
B_speed = 0
B_count = 0
g_pitch = 0   
g_roll = 0

#-------  Section to set up Interrupts ----------
def isr_motorA(dummy):	# motor A sensor ISR - just count transitions
	global A_count
	A_count += 1

def isr_motorB(dummy):	# motor B sensor ISR - just count transitions
	global B_count
	B_count += 1
		
def isr_speed_timer(dummy): 	# timer interrupt at 100msec intervals
	global A_count
	global A_speed
	global B_count
	global B_speed
	A_speed = A_count			# remember count value
	B_speed = B_count
	A_count = 0					# reset the count
	B_count = 0
	
# Create external interrupts for motorA Hall Effect Senor
import micropython
micropython.alloc_emergency_exception_buf(100)
from pyb import ExtInt

motorA_int = ExtInt ('Y4', ExtInt.IRQ_RISING, Pin.PULL_NONE,isr_motorA)
motorB_int = ExtInt ('Y6', ExtInt.IRQ_RISING, Pin.PULL_NONE,isr_motorB)

# Create timer interrupts at 100 msec intervals
speed_timer = pyb.Timer(4, freq=10)
speed_timer.callback(isr_speed_timer)

last_A_speed = 0
A_accel = 0

last_B_speed = 0
B_accel = 0

PID_controller = PIDm(0.7,0.01,0.1)

tic = pyb.millis()
try:
	while True:
		toc = pyb.millis()
		read_imu(toc-tic)

		target_speed = int(get_pitch)

		if toc-tic>5:
			d_A = A_speed - last_A_speed
			d_B = B_speed - last_B_speed
			d_T = (toc - tic) * 0.001

			A_accel = d_A/d_T
			print(A_accel)
			B_accel = d_B/d_T
			last_A_speed = A_speed
			last_B_speed = B_speed

			results = PID_controller.get_pwm(target_speed, A_speed, A_accel, B_speed, B_accel, d_T)

			if results[0] > 0:
				A_forward(results[0])
			else:
				A_back(abs(results[0]))
			
			if results[1] > 0:
				B_forward(results[1])
			else:
				B_back(abs(results[1]))

			oled.draw_text(0,10,'Target Speed:{:5.2f}'.format((target_speed/39)))
			oled.draw_text(0,20,'PWM A:{:5.2f}'.format(results[0]))
			oled.draw_text(0,30,'PWM B:{:5.2f}'.format(results[1]))
			oled.draw_text(0,40,'Motor A:{:5.2f} rps'.format(A_speed/39))	
			oled.draw_text(0,50,'Motor B:{:5.2f} rps'.format(B_speed/39))	
			oled.display()


finally:
	A_stop()
	B_stop()


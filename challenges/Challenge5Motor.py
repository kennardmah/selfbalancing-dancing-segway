
import pyb
from pyb import Pin, Timer
import micropython
micropython.alloc_emergency_exception_buf(100)
from pyb import ExtInt

class MOTOR(object):

	def __init__(self):
		# set up motor with PWM and timer control
		self.A1 = Pin('X3',Pin.OUT_PP)	# A is right motor
		self.A2 = Pin('X4',Pin.OUT_PP)
		self.B1 = Pin('X7',Pin.OUT_PP)	# B is left motor
		self.B2 = Pin('X8',Pin.OUT_PP)
		self.PWMA = Pin('X1')			
		self.PWMB = Pin('X2')
		
		# Configure timer to provide PWM signal
		self.tim = Timer(2, freq = 1000)
		self.motorA = self.tim.channel(1, Timer.PWM, pin = self.PWMA)
		self.motorB = self.tim.channel(2, Timer.PWM, pin = self.PWMB)

		self.A_sense = Pin('Y4', Pin.PULL_NONE)      # Pin.PULL_NONE sets it up as an input pi
		self.B_sense = Pin('Y6', Pin.PULL_NONE)		

		self.A_speed = 0
		self.A_count = 0
		self.B_speed = 0
		self.B_count = 0

		self.motorA_int = ExtInt('Y4', ExtInt.IRQ_RISING, Pin.PULL_NONE, self.isr_motorA)     # ISR runs when Rising Edge of Pin Y4
		self.motorB_int = ExtInt('Y6', ExtInt.IRQ_RISING, Pin.PULL_NONE, self.isr_motorB)

		speed_timer = pyb.Timer(4, freq=10)
		speed_timer.callback(self.isr_speed_timer)		

	#-------  Section to set up Interrupts ----------
	def isr_motorA(self, dummy):	# motor A sensor ISR - just cotransitions
		global A_count
		self.A_count += 1

	def isr_motorB(self, dummy):	# motor B sensor ISR - just count tra
		global B_count
		self.B_count += 1
			
	def isr_speed_timer(self, dummy): 	# timer interrupt at 100msec intervals
		global A_count
		global A_speed
		global B_count
		global B_speed
		self.A_speed = self.A_count			# remember count value
		self.B_speed = self.B_count
		self.A_count = 0					# reset the count
		self.B_count = 0
		

	def A_forward(self, value):
		self.A1.low()
		self.A2.high()
		self.motorA.pulse_width_percent(value)

	def A_back(self, value):
		self.A2.low()
		self.A1.high()
		self.motorA.pulse_width_percent(value)
		
	def A_stop(self):
		self.A1.high()
		self.A2.high()
		
	def B_forward(self, value):
		self.B2.low()
		self.B1.high()
		self.motorB.pulse_width_percent(value)

	def B_back(self, value):
		self.B1.low()
		self.B2.high()
		self.motorB.pulse_width_percent(value)
		
	def B_stop(self):
		self.B1.high()
		self.B2.high()
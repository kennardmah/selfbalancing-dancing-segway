import pyb
from pyb import Pin, Timer, ADC, DAC, LED
from array import array			# need this for memory allocation to buffers
from oled_938 import OLED_938	# Use OLED display driver
from audio import MICROPHONE
from neopixel import NeoPixel
from dance_choreo import dancemove

np = NeoPixel(Pin("Y12", Pin.OUT), 8)

#  The following two lines are needed by micropython
#   ... must include if you use interrupt in your program
import micropython
micropython.alloc_emergency_exception_buf(100)

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
i2c = pyb.I2C(2, pyb.I2C.MASTER)
devid = i2c.scan()				# find the I2C device number
oled = OLED_938(
    pinout={"sda": "Y10", "scl": "Y9", "res": "Y8"},
    height=64,
    external_vcc=False,
    i2c_devid=i2c.scan()[0],
)
oled.poweron()
oled.init_display()
oled.draw_text(0,0, 'Beat Detection')
oled.display()

# define ports for microphone, LEDs and trigger out (X5)

b_LED = LED(4)		# flash for beats on blue LED

def flash():		# routine to flash blue LED when beat detected
	b_LED.on()
	pyb.delay(10)
	b_LED.off()

# Create timer interrupt - one every 1/8000 sec or 125 usec
pyb.disable_irq()
sample_timer = pyb.Timer(7, freq=8000)	# set timer 7 for 8kHz

N = 160				# number of sample to calculate instant energy
mic = ADC(Pin('Y11'))
audio = MICROPHONE(sample_timer, mic, N)
pyb.enable_irq(True)
oled.draw_text(0,20, 'Ready to GO')	# Useful to show what's happening?
oled.display()
pyb.delay(100)

# Calculate energy over 50 epochs, each 20ms (i.e. 1 sec)
M = 50						# number of instantaneous energy epochs to sum
BEAT_THRESHOLD = 2.0		# threshold for c to indicate a beat
MIN_BEAT_PERIOD = 500	# no beat less than this

# initialise variables for main program loop
e_ptr = 0					# pointer to energy buffer
e_buf = array('L', 0 for i in range(M))	# reserve storage for energy buffer
sum_energy = 0				# total energy in last 50 epochs

tic = pyb.millis()			# mark time now in msec
i=0

try:
	while True:				# Main program loop
		if audio.buffer_is_filled():		# semaphore signal from ISR - set if buffer is full

			# Fetch instantaneous energy
			E = audio.inst_energy()			# fetch instantenous energy
			audio.reset_buffer()			# get ready for next epoch

			# compute moving sum of last 50 energy epochs with circular buffer
			sum_energy = sum_energy - e_buf[e_ptr] + E
			e_buf[e_ptr] = E			# over-write earliest energy with most recent
			e_ptr = (e_ptr + 1) % M		# increment e_ptr with wraparound - 0 to M-1
			average_energy = sum_energy/M

			# Compute ratio of instantaneous energy/average energy
			c = E/average_energy
			
			if (pyb.millis()-tic > MIN_BEAT_PERIOD):	# if longer than minimum period
				if (c>BEAT_THRESHOLD) or pyb.millis()-tic > 600:	    # look for a beat or execute if beat is not found
						level = 25# determine the intensity of the movements
						dancemove(i, level)    # execute move depending on counter
						i += 1                  # prepare next move                     
						for i2 in range(8):  # turn LEDs red one at a time
							np[i2] = (64-8*i, 8*i, 8*i)
							np.write()
							pyb.delay(50)				# beat found, flash blue LED
						for i2 in range(8):  # all LEDs dark
							np[i2] = (0, 0, 0)
							np.write()
							pyb.delay(50)
						tic = pyb.millis()      # reset timer  
						if i == 11:
							i=1

				audio.reset_buffer()				# reset status flag

finally:
	dancemove(77, 1)

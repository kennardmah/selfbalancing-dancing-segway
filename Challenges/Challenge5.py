
import pyb, time
from pyb import Pin
from oled_938 import OLED_938          
from mpu6050 import MPU6050
from Challenge5Motor import MOTOR
from Challenge5PID import PID

# Create an IMU object
imu = MPU6050(1, False)

pot = pyb.ADC(Pin('X11'))

# Create an OLED display object (128x64 pixels)...
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height=64, external_vcc=False, i2c_devid=60)
oled.poweron()                          # Turn on the display
oled.init_display()                     # Initialise the display
oled.draw_text(0, 0, 'challenge 3')
oled.display()

motor_instance = MOTOR()

trigger = pyb.Switch()
scale = 20.0
while not trigger():
    time.sleep(0.001)
    Kp = pot.read() * scale / 4095
    oled.draw_text(0,30,'Kp = {:5.2f}'.format(Kp))
    oled.display()
while trigger(): pass
while not trigger():
    time.sleep(0.001)
    Ki = pot.read() * 100 / 4095
    oled.draw_text(0, 30, 'Ki = {:5.2f}'.format(Ki))
    oled.display()
while trigger(): pass
while not trigger():
    time.sleep(0.001)
    Kd = pot.read() * -(3) / 4095
    oled.draw_text(0, 30, 'Kd = {:5.2f}'.format(Kd))
    oled.display()
while trigger(): pass
while not trigger():
    time.sleep(0.001)
    set_point = pot.read() * -(3) / 4095
    oled.draw_text(0, 30, 'Kd = {:5.2f}'.format(Kd))
    oled.display()
while trigger(): pass
print('Button pressed. Running script')
oled.draw_text(0,20,'Running')
oled.draw_text(0, 30, 'Kp{:5.2f}'.format(Kp))
oled.draw_text(0, 40, 'Ki{:5.2f}'.format(Ki))
oled.draw_text(0, 50, 'Kd{:5.2f}'.format(Kd))
oled.display()

def pitch_estimate(pitch, dt, alpha):
    theta = imu.pitch()
    pitch_dot = imu.get_gy()
    pitch = alpha*(pitch+pitch_dot*dt) + (1-alpha)*theta
    return (pitch, pitch_dot)

PID_controller = PID(12,21,-1)

motor_offset = 1
filtered_pitch = 0                 
alpha = 0.99 
set_point = 1.5
output = 0
filtered_pitch = 0

tic = pyb.millis()
try:         
    while True:  
        dt = pyb.millis() - tic 
        filtered_pitch, pitch_dot = pitch_estimate(filtered_pitch, dt*0.001, alpha)
        output = PID_controller.get_pwm(set_point, filtered_pitch, pitch_dot, dt)
        speed = output
        if (speed > 0) :
            motor_instance.B_back(speed)
            motor_instance.A_back(motor_offset*speed)
        elif (speed < 0) :
            motor_instance.B_forward(-speed)
            motor_instance.A_forward(-motor_offset*speed)          
        tic = pyb.millis()

finally:
    motor_instance.A_stop()
    motor_instance.B_stop()

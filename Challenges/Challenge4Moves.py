from Amotor import MOTOR

motor = MOTOR()

def dancemove(i, level = 25): # default level is set to 25
    l = level
    if i == 1:
        motor.A_forward(l)
        motor.B_forward(l/3)
    elif i == 2:
        motor.B_forward(l)
        motor.A_forward(l/3)
    elif i == 3:
        motor.A_stop()
        motor.B_forward(l)
    elif i == 4:
        motor.B_stop()
        motor.A_forward(l)
    elif i == 5:
        motor.A_back(l)
        motor.B_back(l)
    elif i == 6:
        motor.A_forward(l)
        motor.B_forward(l/3)
    elif i == 7:
        motor.B_forward(l)
        motor.A_forward(l/3)
    elif i == 8:
        motor.A_stop()
        motor.B_forward(l)
    elif i == 9:
        motor.B_stop()
        motor.A_forward(l)
    elif i == 10:
        motor.A_forward(l)
        motor.B_forward(l)
    elif i == 11:
        i = 0
    elif i == 77:
        motor.A_stop(l)
        motor.B_stop(l)
    else:
        motor.A_stop()
        motor.B_stop()
    

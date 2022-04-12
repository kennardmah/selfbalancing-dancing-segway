class PIDm():
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        self.A_totalError = 0
        self.B_totalError = 0
        
    def get_pwm(self, target, A, dA, B, dB, dT):
        A_error = target - A
        B_error = target - B
        
        A_integrator = self.A_totalError + (A_error * dT) 
        B_integrator = self.B_totalError + (B_error * dT)

        A_output = self.Kp * A_error + self.Ki * A_integrator + self.Kd * dA
        B_output = self.Kp * B_error + self.Ki * B_integrator + self.Kd * dB

        self.A_totalError += A_error
        self.B_totalError += B_error

        A_pwm = target + A_output
        B_pwm = target + B_output

        A_pwm = max(min(A_pwm, 100),-100)
        B_pwm = max(min(B_pwm, 100),-100)

        return (A_pwm, B_pwm)



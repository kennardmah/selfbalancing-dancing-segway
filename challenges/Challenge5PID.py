class PID(object):
    def __init__(self, KP, KI, KD):
        self.KP = KP
        self.KI = KI
        self.KD = KD

    def get_pwm(self, set_point, cfilter_pitch, rate_pitch, dt):
        Error = set_point - cfilter_pitch
        dError = rate_pitch
        intError = Error*dt

        output = self.KP*Error + self.KI*intError + self.KD*dError
        output = max(min(output, 100), -100)
        return output


    # def PID(set_point, curr_pitch, r_pitch, dt):
    # error = set_point - curr_pitch
    # error_dev = r_pitch
    # error_int = error*dt

    # P = 12*error
    # I = 21*error_int
    # D = -1*error_dev

    # PID = P + I + D
    # output = max(min(PID, 100), -100)
    # return output
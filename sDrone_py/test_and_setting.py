class UnitMotor:
    def __init__(self, name_motor):
        self.name = name_motor
        self.pwm = 0.4
        print("Мотор {0} инициализован, значение PWM {1}", self.name, self.pwm)

    def set_motor_power(self, pwm):
        self.pwm = pwm
        print("PWM={0}", self.pwm)

from sDrone_py import orientationCopter as Ax


class Motor:
    __pwm = 0
    __name = ""
    __i_param = 0
    __old_error = 0
    __pin = 0
    __kp = 0
    __ki = 0
    __kd = 0
    __axis = ""
    __pid = 0
    __error = 0

    def __init__(self, name, pin, pwm, axis):
        self.__name = name
        self.__pwm = pwm
        self.__pin = pin
        self.__axis = axis

    def set_pwm(self, pwm):
        self.__pwm = pwm
        print(pwm)

    def set_name(self, name):
        self.__name = name

    def set_i_param(self, i_param):
        self.__i_param = i_param

    def set_old_error(self, old_error):
        self.__old_error = old_error

    def set_axis(self, axis):
        self.__axis = axis

    def set_pin(self, pin):
        self.__pin = pin

    def set_pid_coefficient(self, kp, ki, kd):
        self.__ki = ki
        self.__kp = kp
        self.__kd = kd

    def set_pid_critical_stop(self, value):
        self.__pid = value

    def get_pwm(self):
        return self.__pwm

    def get_name(self):
        return self.__name

    def get_i_param(self):
        return self.__i_param

    def get_old_error(self):
        return self.__old_error

    def get_pin(self):
        return self.__pin

    def gen_report(self):
        arr = {(self.get_pin(), self.get_pwm(), self.__axis): self.get_name()}
        return arr

    def get_axis(self):
        return self.__axis

    def get_pid(self):
        return self.__pid

    def get_pid_coefficient(self):
        args = {"p": self.__kp, "i": self.__ki, "d": self.__kd}
        return args

    def get_error(self):
        return self.__error

    def get_error_for_pid(self, real_pos):

        if self.get_axis() == "OY":  # "так как берем значения оси X"
            error = real_pos - Ax.get_ox()
            print("ox: s%", Ax.get_ox())

            if error < 0:
                if self.get_name() == "BR":
                    error = 0
            else:
                if self.get_name() == "FL":
                    error = 0
        else:
            error = real_pos - Ax.get_oy()
            print("oy: s%", Ax.get_oy())
            if error < 0:
                if self.get_name() == "FR":
                    error = 0
            else:
                if self.get_name() == "BL":
                    error = 0

        if -1 <= error < 0:
            error = 0
        elif 1 > error > 0:
            error = 0

        return int(error)

    def pid(self, i_max, i_min, real_pos, t_step):
        er = self.get_error_for_pid(real_pos)
        self.__error = er
        # print("Error " + self.get_name(), er)
        self.__i_param += er

        if self.__i_param < i_min:
            self.__i_param = i_min
        elif self.__i_param > i_max:
            self.__i_param = i_max

        p_term = float(format(self.__kp * er, '.3f'))
        i_term = float(format((self.__ki * float(format(self.__i_param, '.5f'))) * t_step, '.5f'))
        d_term = float(format((self.__kd * (self.get_error_for_pid(real_pos) - self.__old_error)) / t_step, '.3f'))
        temp_pid = p_term + i_term + d_term
        self.__old_error = er 

        if temp_pid < 0:
            if self.get_name() == "BL" or self.get_name() == "FL":
                temp_pid *= -1

        self.__pid = float(format(temp_pid, '.3f'))
        # print("PID " + self.get_name(), self.get_pid())
        # return float(format(temp_pid, '.3f'))

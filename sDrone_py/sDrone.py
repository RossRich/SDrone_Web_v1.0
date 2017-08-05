import webiopi
from sDrone_py import orientationCopter as ax
import time as t

IO = webiopi.GPIO
# DEFAULT_MAX_SIGNAL = 0.1
# DEFAULT_MIN_SIGNAL = 0.04
I_MAX = int(5)
I_MIN = int(-5)
T_STEP = 0.08  # 1s=1000ms
stick_angle_y = 0
stick_angle_x = 0
stick_pos = DEFAULT_MIN_SIGNAL
flag_roll_position_x = 0
flag_roll_position_y = 0
i_state = 0
d_state = 0
old_error = 0
pid = 0
FLAG = 0
MOTOR_PIN_FL = int(18)
MOTOR_PIN_FR = int(17)
MOTOR_PIN_BL = int(27)
MOTOR_PIN_BR = int(22)
global_drive_controller = 0


def error_x_y(position):
    error_y = position - get_angle()
    print("error: ", error_y)
    return error_y


def get_angle():
    y_angle = float(format(ax.get_oy(), '.0f'))
    return y_angle


def get_angle_x():
    x_angle = float(format(ax.get_ox(), '.0f'))
    return x_angle


def update_pid(kp, ki, kd):
    global i_state, old_error

    error=0

    if  flag_roll_position_x>1.7:

    if stick_pos > DEFAULT_MIN_SIGNAL or stick_pos < DEFAULT_MAX_SIGNAL:
        i_state += er

        if i_state < I_MIN:
            i_state = I_MIN
        elif i_state > I_MAX:
            i_state = I_MAX

    print("\ni_state=", i_state)
    p_term = float(format(kp * er, '.3f'))
    i_term = float(format((ki * float(format(i_state, '.5f'))) * T_STEP, '.5f'))
    d_term = float(format((kd * (error_x_y(stick_angle_y) - old_error)) / T_STEP, '.3f'))
    print("*P=%s\t*I=%s\t*D=%s" % (p_term, i_term, d_term))
    temp_pid = p_term + i_term + d_term
    old_error = er
    Upid = temp_pid

    return float(format(Upid, '.3f'))


def left_drive(d_l):
    IO.pulseRatio(MOTOR_PIN_FL, d_l)
    IO.pulseRatio(MOTOR_PIN_BL, d_l)


def right_drive(d_r):
    IO.pulseRatio(MOTOR_PIN_FR, d_r)
    IO.pulseRatio(MOTOR_PIN_BR, d_r)


def front_drive(f_d):
    IO.pulseRatio(MOTOR_PIN_FR, f_d)
    IO.pulseRatio(MOTOR_PIN_FL, f_d)


def back_drive(b_d):
    IO.pulseRatio(MOTOR_PIN_BR, b_d)
    IO.pulseRatio(MOTOR_PIN_BL, b_d)


def normalisation(d_value):
    global global_drive_controller
    if d_value < stick_pos:
        d_value = stick_pos
    elif d_value > DEFAULT_MAX_SIGNAL:
        d_value = DEFAULT_MAX_SIGNAL
    global_drive_controller = d_value
    return float(format(d_value, '.2f'))


def drive_controller():
    if FLAG:
        if flag_roll_position == 1:
            d_l = stick_pos + pid
            left_drive(normalisation(d_l))
        elif flag_roll_position == -1:
            t_pid = pid * (-1)
            d_r = stick_pos + t_pid
            right_drive(normalisation(d_r))
        elif flag_roll_position == 0:
            print("HOR\n")
    else:
        print("wait")


def go_motor(set_power_motor_go):
    IO.pulseRatio(MOTOR_PIN_FL, set_power_motor_go)
    IO.pulseRatio(MOTOR_PIN_FR, set_power_motor_go)
    IO.pulseRatio(MOTOR_PIN_BL, set_power_motor_go)
    IO.pulseRatio(MOTOR_PIN_BR, set_power_motor_go)


@webiopi.macro
def go():
    global FLAG
    go_motor(stick_pos)
    if stick_pos <= 0.05:
        FLAG = 0
        go_motor(DEFAULT_MIN_SIGNAL)
    else:
        FLAG = 1


@webiopi.macro
def start_unit(name, power):
    name = name.upper()
    print(name, power)
    if name == "FL":
        IO.pulseRatio(MOTOR_PIN_FL, float(power))
    elif name == "FR":
        IO.pulseRatio(MOTOR_PIN_FR, float(power))
    elif name == "BR":
        IO.pulseRatio(MOTOR_PIN_BR, float(power))
    elif name == "BL":
        IO.pulseRatio(MOTOR_PIN_BL, float(power))
    elif name == "ALL":
        go_motor(float(power))
    else:
        pass


@webiopi.macro
def set_power(power):
    global stick_pos
    stick_pos = float(power)


def setup():
    IO.setFunction(MOTOR_PIN_FL, IO.PWM)
    IO.setFunction(MOTOR_PIN_FR, IO.PWM)
    IO.setFunction(MOTOR_PIN_BR, IO.PWM)
    IO.setFunction(MOTOR_PIN_BL, IO.PWM)
    go_motor(DEFAULT_MIN_SIGNAL)


def get_axis():
    global flag_roll_position_x, flag_roll_position_y

    if get_angle_x() >= 1.7:
        flag_roll_position_x = int(1)  # front
    elif get_angle_x() <= -1.7:
        flag_roll_position_x = int(-1)  # back
    else:
        flag_roll_position_x = 0

    if get_angle_y() >= 1.7:
        flag_roll_position_y = int(1)  # left
    elif get_angle_y() <= -1.7:
        flag_roll_position_y = int(-1)  # right
    else:
        flag_roll_position_y = 0


def test():
    if flag_roll_position_x > 0:


def loop():
    global pid
    get_axis()
    test()
    pid = update_pid(0.0005, 0.0000065, 0.000075)
    print("pid: ", pid)
    print("drive_controller: ", global_drive_controller)
    drive_controller()
    t.sleep(T_STEP)
    ax.cls()


def destroy():
    global FLAG
    FLAG = 0
    go_motor(DEFAULT_MIN_SIGNAL)
    IO.setFunction(MOTOR_PIN_FL, IO.IN)
    IO.setFunction(MOTOR_PIN_FR, IO.IN)
    IO.setFunction(MOTOR_PIN_BR, IO.IN)
    IO.setFunction(MOTOR_PIN_BL, IO.IN)

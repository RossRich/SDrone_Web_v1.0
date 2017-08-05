from sDrone_py.Class_motor import Motor
import time as t
import sDrone_py.search_step as step
import webiopi as wip

from sDrone_py.orientationCopter import cls, print_all

IO = wip.GPIO
DEFAULT_MAX_SIGNAL = 0.095
DEFAULT_MIN_SIGNAL = 0.04
I_MAX = int(2)
I_MIN = int(-2)
T_STEP = 0.025  # 1s=1000ms
# stick_power = 0  # power
# stick_angle = 0  # angle
MOTOR_PIN_FL = int(18)
MOTOR_PIN_FR = int(17)
MOTOR_PIN_BL = int(27)
MOTOR_PIN_BR = int(22)
angle_left = 0
angle_right = 0
critical_flag = False
P_TERM = 0.00001  # 0.0000881  # 0006
I_TERM = 0.0  # 0.00000775  # 0000075
D_TERM = 0.00000985  # 0.00002122  # 000085
mode = "realise"
debug_axis = ""


@wip.macro
def set_power(power):
    # global stick_power
    stick_power = float(power)
    MOTOR_FL_Y.set_pwm(stick_power)
    MOTOR_FR_X.set_pwm(stick_power)
    MOTOR_BL_X.set_pwm(stick_power)
    MOTOR_BR_Y.set_pwm(stick_power)


@wip.macro
def left(val_l):
    global angle_left
    angle_left = int(val_l)
    # MOTOR_FL_Y.pid(I_MAX, I_MIN, angle_left, T_STEP)
    # MOTOR_BL_X.pid(I_MAX, I_MIN, angle_left, T_STEP)
    print(angle_left)


@wip.macro
def right(val_r):
    global angle_right
    angle_right = int(val_r)
    # MOTOR_FR_X.pid(I_MAX, I_MIN, angle_right, T_STEP)
    # MOTOR_BR_Y.pid(I_MAX, I_MIN, angle_right, T_STEP)
    print(angle_right)


@wip.macro
def back(val_b):
    global angle_back
    angle_back = int(val_b)
    # MOTOR_BL_X
    # MOTOR_BR_Y


@wip.macro
def front(val_f):
    global angle_front
    angle_front = int(val_f)
    # MOTOR_FL_Y
    # MOTOR_FR_X


@wip.macro
def start_debug_motors(power):
    print("*start_debug. Set PWM_3")
    power = float(power)
    if debug_axis == "ox":
        MOTOR_BL_X.set_pwm(power)
        MOTOR_FR_X.set_pwm(power)
    elif debug_axis == "oy":
        MOTOR_FL_Y.set_pwm(power)
        MOTOR_BR_Y.set_pwm(power)
    else:
        print("INVALID ARGUMENT")


@wip.macro
def critical_stop():
    print("*stop")
    global critical_flag
    if critical_flag:
        critical_flag = False
        MOTOR_FL_Y.set_pid_critical_stop(0)
        MOTOR_BL_X.set_pid_critical_stop(0)
        MOTOR_FR_X.set_pid_critical_stop(0)
        MOTOR_BR_Y.set_pid_critical_stop(0)
        set_power(DEFAULT_MIN_SIGNAL)
        gas()
    else:
        critical_flag = True


@wip.macro
def debug_pid(val_p, val_i, val_d):
    print("*debug_pid.Set p,i,d_4")
    p = float(val_p)
    # print(p)
    i = float(val_i)
    # print(i)
    d = float(val_d)
    # print(d)
    if debug_axis == "ox":
        MOTOR_BL_X.set_pid_coefficient(p, i, d)
        MOTOR_FR_X.set_pid_coefficient(p, i, d)
    elif debug_axis == "oy":
        MOTOR_FL_Y.set_pid_coefficient(p, i, d)
        MOTOR_BR_Y.set_pid_coefficient(p, i, d)
    else:
        print("INVALID ARGUMENT")


@wip.macro
def get_param(debug_axis_js):
    print("*debug. Get_param_2")
    global debug_axis
    debug_axis = debug_axis_js
    args = {}
    if debug_axis == "ox":
        args = MOTOR_FR_X.get_pid_coefficient()
    elif debug_axis == "oy":
        args = MOTOR_FL_Y.get_pid_coefficient()
    else:
        print("INVALID ARGUMENT")
    out_step = step.processing(**args)
    return out_step


@wip.macro
def set_mode(mode_js):
    global mode
    mode = mode_js
    print("*set_mode_1: ", mode)
    t.sleep(2)


def test():
    print("P:%s ,I:%s ,D:%s" % (P_TERM, I_TERM, D_TERM))
    print("|Name\t|Pin\t|PWM\t|Axis\t|")

    for i in range(4):
        if i == 0:
            rep_arr = MOTOR_FL_Y.gen_report()
        elif i == 1:
            rep_arr = MOTOR_BR_Y.gen_report()
        elif i == 2:
            rep_arr = MOTOR_BL_X.gen_report()
        elif i == 3:
            rep_arr = MOTOR_FR_X.gen_report()
        else:
            rep_arr = {}

        for key, value in rep_arr.items():
            print("|", value, "\t|", key[0], "\t|", key[1], "\t|", key[2], "\t|")
    t.sleep(1)


def setup():
    global MOTOR_FL_Y, MOTOR_BL_X, MOTOR_BR_Y, MOTOR_FR_X
    MOTOR_FL_Y = Motor("FL", MOTOR_PIN_FL, DEFAULT_MIN_SIGNAL, "OY")
    MOTOR_FR_X = Motor("FR", MOTOR_PIN_FR, DEFAULT_MIN_SIGNAL, "OX")
    MOTOR_BL_X = Motor("BL", MOTOR_PIN_BL, DEFAULT_MIN_SIGNAL, "OX")
    MOTOR_BR_Y = Motor("BR", MOTOR_PIN_BR, DEFAULT_MIN_SIGNAL, "OY")
    MOTOR_FL_Y.set_pid_coefficient(P_TERM, I_TERM, D_TERM)
    MOTOR_FR_X.set_pid_coefficient(P_TERM, I_TERM, D_TERM)
    MOTOR_BL_X.set_pid_coefficient(P_TERM, I_TERM, D_TERM)
    MOTOR_BR_Y.set_pid_coefficient(P_TERM, I_TERM, D_TERM)
    IO.setFunction(MOTOR_FL_Y.get_pin(), IO.PWM)
    IO.setFunction(MOTOR_FR_X.get_pin(), IO.PWM)
    IO.setFunction(MOTOR_BR_Y.get_pin(), IO.PWM)
    IO.setFunction(MOTOR_BL_X.get_pin(), IO.PWM)
    test()
    gas()


def normalisation(d_value):
    if d_value <= DEFAULT_MIN_SIGNAL:
        d_value = DEFAULT_MIN_SIGNAL
    elif d_value >= DEFAULT_MAX_SIGNAL:
        d_value = DEFAULT_MAX_SIGNAL
    return float(format(d_value, '.3f'))


def gas():
    m1 = MOTOR_FL_Y.get_pwm()
    m2 = MOTOR_BL_X.get_pwm()
    m3 = MOTOR_FR_X.get_pwm()
    m4 = MOTOR_BR_Y.get_pwm()

    m1 += MOTOR_FL_Y.get_pid()
    con1 = normalisation(m1)
    IO.pulseRatio(MOTOR_FL_Y.get_pin(), con1)

    m2 += MOTOR_BL_X.get_pid()
    con2 = normalisation(m2)
    IO.pulseRatio(MOTOR_BL_X.get_pin(), con2)

    m3 += MOTOR_FR_X.get_pid()
    con3 = normalisation(m3)
    IO.pulseRatio(MOTOR_FR_X.get_pin(), con3)

    m4 += MOTOR_BR_Y.get_pid()
    con4 = normalisation(m4)
    IO.pulseRatio(MOTOR_BR_Y.get_pin(), con4)

    print("BR ", normalisation(m4), '\t', "BL ", normalisation(m2), '|\t',
          "FR ", normalisation(m3), '\t', "FL ", normalisation(m1))


def debug_function(axis):
    cls()
    print("*main_debug. processing")

    if axis == "ox":
        debug_m1 = MOTOR_BL_X.get_pwm()
        debug_m2 = MOTOR_FR_X.get_pwm()
        debug_pid1 = MOTOR_BL_X.get_pid()
        debug_pid2 = MOTOR_FR_X.get_pid()
        print("get_pid_x: ", MOTOR_BL_X.get_pid_coefficient())
    elif axis == "oy":
        debug_m1 = MOTOR_FL_Y.get_pwm()
        debug_m2 = MOTOR_BR_Y.get_pwm()
        debug_pid1 = MOTOR_FL_Y.get_pid()
        debug_pid2 = MOTOR_BR_Y.get_pid()
        print("get_pid_y: ", MOTOR_BR_Y.get_pid_coefficient())
    else:
        debug_m1 = DEFAULT_MIN_SIGNAL
        debug_m2 = DEFAULT_MIN_SIGNAL
        debug_pid1 = 0
        debug_pid2 = 0
        print("INVALID ARGUMENT")

    debug_control_1 = debug_m1 + debug_pid1
    debug_control_2 = debug_m2 + debug_pid2
    debug_control_1 = normalisation(debug_control_1)
    debug_control_2 = normalisation(debug_control_2)

    print("+--------pid---------pwm--------------sped------------------------------+")
    print("|pid: %s\t%s\t|pwm: %s\t%s\t|sped: %s\t%s\t|"
          % (float(debug_pid1), float(debug_pid2), float(debug_m1), float(debug_m2), float(debug_control_1),
             float(debug_control_2)))
    print("+-----------------------------------------------------------------------+")
    if axis == "ox":
        IO.pulseRatio(MOTOR_BL_X.get_pin(), debug_control_1)
        IO.pulseRatio(MOTOR_FR_X.get_pin(), debug_control_2)
    elif axis == "oy":
        IO.pulseRatio(MOTOR_FL_Y.get_pin(), debug_control_1)
        IO.pulseRatio(MOTOR_BR_Y.get_pin(), debug_control_2)
    else:
        print("INVALID ARGUMENT")


def loop():
    # cls()
    print_all()
    MOTOR_FL_Y.pid(I_MAX, I_MIN, angle_left, T_STEP)
    MOTOR_BL_X.pid(I_MAX, I_MIN, angle_left, T_STEP)
    MOTOR_FR_X.pid(I_MAX, I_MIN, angle_right, T_STEP)
    MOTOR_BR_Y.pid(I_MAX, I_MIN, angle_right, T_STEP)
    if critical_flag and mode == "realise":
        gas()
    elif critical_flag and mode == "debug":
        debug_function(debug_axis)
    else:
        pass
    t.sleep(T_STEP)


def destroy():
    set_power(DEFAULT_MIN_SIGNAL)
    gas()
    IO.setFunction(MOTOR_FL_Y.get_pin(), IO.IN)
    IO.setFunction(MOTOR_FR_X.get_pin(), IO.IN)
    IO.setFunction(MOTOR_BR_Y.get_pin(), IO.IN)
    IO.setFunction(MOTOR_BL_X.get_pin(), IO.IN)

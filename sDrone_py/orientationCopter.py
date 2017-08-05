import smbus
import math
import time as t
import os

POWER_MGMT_1 = 0x6b
POWER_MGMT_2 = 0x6c

ADDRESS_I2C = 0x68  # This is the address value read via the i2cdetect command
ADDRESS_GYRO_X_OUT = 0x43
ADDRESS_GYRO_Y_OUT = 0x45
ADDRESS_GYRO_Z_OUT = 0x47
ADDRESS_ACCEL_X_OUT = 0x3b
ADDRESS_ACCEL_Y_OUT = 0x3d
ADDRESS_ACCEL_Z_OUT = 0x3f
ADDRESS_TEMP = 0x41

GYRO_VALUE = 131.0
ACCEL_VALUE = 16384.0
TEMP_VALUE = 24.87

bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards
bus.write_byte_data(ADDRESS_I2C, POWER_MGMT_1, 0)


# def read_byte(adr):
#     return bus.read_byte_data(ADDRESS_I2C, adr)


def read_word_2c(adr):
    high = bus.read_byte_data(ADDRESS_I2C, adr)
    low = bus.read_byte_data(ADDRESS_I2C, adr + 1)
    read_word = (high << 8) + low
    # val = read_word(adr)
    if read_word >= 0x8000:
        return -((65535 - read_word) + 1)
    else:
        return read_word


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_x_rotation(x, y, z):
    radians_x = math.atan2(y, dist(x, z))
    x_rot = math.degrees(radians_x)
    return x_rot


def get_y_rotation(x, y, z):
    radians_y = math.atan2(x, dist(y, z))
    y_rot = -(math.degrees(radians_y))
    return y_rot


def get_temperature():
    word_2c = read_word_2c(ADDRESS_TEMP)
    temp = (word_2c / 154) + TEMP_VALUE
    return temp


def get_gyro_x():
    tmp_x_out = read_word_2c(ADDRESS_GYRO_X_OUT)
    gyro_x = tmp_x_out / GYRO_VALUE
    return gyro_x


def get_gyro_y():
    tmp_y_out = read_word_2c(ADDRESS_GYRO_Y_OUT)
    gyro_y = tmp_y_out / GYRO_VALUE
    return gyro_y


def get_gyro_z():
    tmp_z_out = read_word_2c(ADDRESS_GYRO_Z_OUT)
    gyro_z = tmp_z_out / GYRO_VALUE
    return gyro_z


def get_accel_x():
    tmp_x_out = read_word_2c(ADDRESS_ACCEL_X_OUT)
    accel_x = tmp_x_out / ACCEL_VALUE
    return accel_x


def get_accel_y():
    tmp_y_out = read_word_2c(ADDRESS_ACCEL_Y_OUT)
    accel_y = tmp_y_out / ACCEL_VALUE
    return accel_y


def get_accel_z():
    tmp_z_out = read_word_2c(ADDRESS_ACCEL_Z_OUT)
    accel_z = tmp_z_out / ACCEL_VALUE
    return accel_z


def get_ox():
    xX = get_accel_x()
    yX = get_accel_y()
    zX = get_accel_z()
    ox = get_x_rotation(xX, yX, zX)
    return ox


def get_oy():
    xY = get_accel_x()
    yY = get_accel_y()
    zY = get_accel_z()
    oy = get_y_rotation(xY, yY, zY)
    return oy


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_all():
    x = float(format(get_ox(), '.0f'))
    y = float(format(get_oy(), '.0f'))
    tem = get_temperature()
    print("OX ", x)
    print("OY ", y)
    print("Temperature MPU ", format(tem, '.1f'))
    # cls()

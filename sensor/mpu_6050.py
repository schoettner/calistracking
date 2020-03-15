import smbus
import math


class MPU6050:

    def __init__(self, i2c_address: int):
        power_mgmt_1 = 0x6b
        power_mgmt_2 = 0x6c
        self.address = i2c_address  # via i2cdetect
        self.bus = smbus.SMBus(1)  # bus = smbus.SMBus(0) for Revision 1

        # activate power
        self.bus.write_byte_data(self.address, power_mgmt_1, 0)

    #########################################################################################
    ################################## READ BYES FROM SENSOR ################################
    #########################################################################################
    def __read_byte__(self, reg):
        return self.bus.read_byte_data(self.address, reg)

    def __read_word__(self, reg):
        h = self.bus.read_byte_data(self.address, reg)
        l = self.bus.read_byte_data(self.address, reg + 1)
        value = (h << 8) + l
        return value

    def __read_word_2c__(self, reg):
        val = self.__read_word__(reg)
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    #########################################################################################
    ################################# READ VALUES FROM SENSOR ###############################
    #########################################################################################

    # all
    def get_data(self):
        x, y, z = self.get_gyro()
        a_x, a_y, a_z = self.get_accelerometer()
        a_x_scale = self.__scale_accelerometer__(a_x)
        a_y_scale = self.__scale_accelerometer__(a_y)
        a_z_scale = self.__scale_accelerometer__(a_z)
        rot_x, rot_y = self.calculate_rotation(a_x_scale, a_y_scale, a_z_scale)
        return x, y, z, a_x, a_y, a_z, rot_x, rot_y

    def print_data(self):
        x, y, z, a_x, a_y, a_z, rot_x, rot_y = self.get_data()
        print('Gyroscope x: {} , y: {} , z: {}'.format(x, y, z))
        print("---------------------")
        print('Accelerometer x: {} , y: {} , z: {}'.format(a_x, a_y, a_z))
        print("---------------------")
        print("Rotation x: {}, y: {}".format(rot_x, rot_y))

    # gyroscope
    def get_gyro(self, scaled: bool = False):
        return self.__get_gyro_x__(scaled), self.__get_gyro_y__(scaled), self.__get_gyro_z__(scaled)

    def __get_gyro_x__(self, scaled: bool = False):
        x = self.__read_word_2c__(0x43)
        return self.__scale_gyro__(x) if scaled else x

    def __get_gyro_y__(self, scaled: bool = False):
        y = self.__read_word_2c__(0x45)
        return self.__scale_gyro__(y) if scaled else y

    def __get_gyro_z__(self, scaled: bool = False):
        z = self.__read_word_2c__(0x47)
        return self.__scale_gyro__(z) if scaled else z

    # accelerometer
    def get_accelerometer(self, scaled: bool = False):
        return self.__get_accel_x__(scaled), self.__get_accel_y__(scaled), self.__get_accel_z__(scaled)

    def __get_accel_x__(self, scaled: bool = False):
        x = self.__read_word_2c__(0x3b)
        return self.__scale_accelerometer__(x) if scaled else x

    def __get_accel_y__(self, scaled: bool = False):
        y = self.__read_word_2c__(0x3d)
        return self.__scale_accelerometer__(y) if scaled else y

    def __get_accel_z__(self, scaled: bool = False):
        z = self.__read_word_2c__(0x3f)
        return self.__scale_accelerometer__(z) if scaled else z

    #########################################################################################
    ################################# CALCULATE SENSOR VALUES ###############################
    #########################################################################################

    @staticmethod
    def __scale_gyro__(value):
        return value / 131

    @staticmethod
    def __scale_accelerometer__(value):
        return value / 16384

    @staticmethod
    def __calculate_distance__(a, b):
        return math.sqrt((a * a) + (b * b))

    def get_rotation(self):
        acceleration = self.get_accelerometer(scaled=True)
        return self.__calc_x_rotation__(*acceleration), self.__calc_y_rotation__(*acceleration)

    def calculate_rotation(self, x, y, z):
        return self.__calc_x_rotation__(x, y, z), self.__calc_y_rotation__(x, y, z)

    def __calc_x_rotation__(self, x, y, z):
        radians = math.atan2(y, self.__calculate_distance__(x, z))
        return math.degrees(radians)

    def __calc_y_rotation__(self, x, y, z):
        radians = math.atan2(x, self.__calculate_distance__(y, z))
        return -math.degrees(radians)

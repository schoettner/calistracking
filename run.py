import argparse

from sensor.mpu_6050 import MPU6050


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--sensor', help='i2c address of NPU5060 sensor', type=int, required=True)
    return parser.parse_args()


def main(args: argparse.Namespace):

    sensor = MPU6050(args.sensor)
    x, y, z = sensor.get_gyro()
    a_x, a_y, a_z = sensor.get_accelerometer()
    rot_x, rot_y = sensor.get_rotation()
    print('Gyroscope x:{} , y:{} , z:{}'.format(x, y, z))
    print("---------------------")
    print('Accelerometer x:{} , y:{} , z:{}'.format(a_x, a_y, a_z))
    print("---------------------")
    print("Rotation x: {}, y: {}".format(rot_x, rot_y))


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

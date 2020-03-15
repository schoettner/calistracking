import argparse

from flask import Flask

from sensor.mpu_6050 import MPU6050
from sensor.sensor_controller import SensorController
from sensor.sensor_service import SensorService


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--sensor', help='i2c address of NPU5060 sensor', type=int, required=True)
    parser.add_argument('--port', help='port on which to start the application', type=int, default=8080)
    return parser.parse_args()


def main(args: argparse.Namespace):
    app = Flask(__name__)
    sensor = MPU6050(args.sensor)
    service = SensorService(sensor)
    controller = SensorController('sensor_controller', __name__, service)
    app.register_blueprint(controller)
    app.run(host='0.0.0.0', port=args.port, debug=True, use_reloader=False)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

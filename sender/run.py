import argparse

from sender.communication.kafka_service import KafkaService
from sender.sensor.mpu_6050_sensor import MPU6050Sensor


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--kafka', help='kafka Bootstrap server', type=str, defualt='localhost:9092')
    return parser.parse_args()


def main(args: argparse.Namespace):
    sensor = MPU6050Sensor()
    service = KafkaService(bootstrap_server=args.kafka)
    while True:
        data = sensor.read_sensor()
        service.send_sensor_data(data)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

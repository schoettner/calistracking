from kafka import KafkaProducer

from dto.sensor_data import SensorData


class KafkaService:

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=['broker1:1234'])
        self.topic = 'sensor_data_v0'

    def send_sensor_data(self, data: SensorData):
        message = data.to_json()
        self.producer.send(topic=self.topic, value=message)


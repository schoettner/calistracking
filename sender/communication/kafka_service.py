from kafka import KafkaProducer
import json

from dto.sensor_data import SensorData


class KafkaService:

    def __init__(self, bootstrap_server: str = 'localhost:9092'):
        self.producer = KafkaProducer(bootstrap_servers=[bootstrap_server],
                                      value_serializer=lambda m: json.dumps(m).encode('ascii'))
        self.topic = 'sensor_data_v0'

    def send_sensor_data(self, data: SensorData):
        message = data.to_json()
        self.producer.send(topic=self.topic, value=message)
        self.producer.flush()


if __name__ == "__main__":
    service = KafkaService()
    dummy = SensorData()
    service.send_sensor_data(dummy)
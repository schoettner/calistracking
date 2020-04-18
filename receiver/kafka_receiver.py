import json

from kafka import KafkaConsumer


class KafkaReceiver:

    @staticmethod
    def create_consumer(
            group_id: str,
            bootstrap_server: str = 'localhost:9092'):
        topic = 'sensor_data_v0'
        return KafkaConsumer(topic,
                             bootstrap_servers=[bootstrap_server],
                             auto_offset_reset='earliest',  # consume from start
                             value_deserializer=lambda m: json.loads(m.decode('ascii')),
                             group_id=group_id)


if __name__ == "__main__":
    consumer = KafkaReceiver.create_consumer('my-test-03', bootstrap_server='192.168.2.108:9092')
    for message in consumer:
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))

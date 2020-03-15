from flask import Blueprint, request

from sensor.sensor_service import SensorService


class SensorController(Blueprint):

    def __init__(self, name, import_name, service: SensorService):
        super().__init__(name, import_name)
        self.service = service
        self.add_url_rule(rule='/record', view_func=self.start_recording, methods=['POST'])
        self.add_url_rule(rule='/hello', view_func=self.hello, methods=['GET'])

    def start_recording(self):
        body = request.get_json(force=True)
        if 'datapoints' in body:
            datapoints = body['datapoints']
        else:
            datapoints=100
        csv = self.service.record_sensor(datapoints=datapoints)
        return 'saved {} data points to {}'.format(datapoints, csv), 200

    def hello(self):
        return 'hello', 200
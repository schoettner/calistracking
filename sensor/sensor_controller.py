from flask import Blueprint, request

from sensor.sensor_service import SensorService


class SensorController(Blueprint):

    def __init__(self, name, import_name, service: SensorService, url_prefix: str = '/api'):
        super().__init__(name, import_name, url_prefix)
        self.service = service
        self.add_url_rule(rule='/record', view_func=self.start_recording)

    def start_recording(self):
        if request.method == 'POST':
            datapoints = request.args.get('values', default=100, type=int)
            csv = self.service.record_sensor(datapoints=datapoints)
            return 'saved {} data points to {}'.format(datapoints, csv), 200
        else:
            return 'Method not allowed', 405

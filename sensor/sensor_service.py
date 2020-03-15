import numpy as np
from sensor.mpu_6050 import MPU6050
from datetime import datetime


class SensorService:

    def __init__(self, sensor: MPU6050):
        self.sensor = sensor
        self.sensor_data_len = 8  # x, y, z, a_x, a_y, a_z, rot_x, rot_y

    def record_sensor(self, datapoints: int = 100) -> str:
        data = np.zeros(shape=(datapoints, self.sensor_data_len), dtype=np.float)
        for i in range(datapoints):
            data[i] = self.sensor.get_data()
        filename = '{}.csv'.format(datetime.utcnow())
        np.savetxt(filename, X=data, delimiter=',')
        return filename

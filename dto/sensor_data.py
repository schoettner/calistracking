from dataclasses import dataclass
from dataclasses_json import dataclass_json
import json
import math

# https://pypi.org/project/dataclasses-json/
@dataclass
@dataclass_json
class SensorData:
    Ax: float
    Ay: float
    Az: float

    Gx: float
    Gy: float
    Gz: float

    def __init__(self,
                 Ax: float = 0,
                 Ay: float = 0,
                 Az: float = 0,
                 Gx: float = 0,
                 Gy: float = 0,
                 Gz: float = 0,
                 ):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
        self.Gx = Gx
        self.Gy = Gy
        self.Gz = Gz

    def print_log(self):
        print("Gx=%.2f" % self.Gx, u'\u00b0' + "/s", "\tGy=%.2f" % self.Gy, u'\u00b0' + "/s", "\tGz=%.2f" % self.Gz,
              u'\u00b0' + "/s", "\tAx=%.2f g" % self.Ax, "\tAy=%.2f g" % self.Ay, "\tAz=%.2f g" % self.Az,
                "\tx_rot=%.2f\u00b0" % self.get_x_rotation(), "\ty_rot=%.2f\u00b0" % self.get_y_rotation())

    @staticmethod
    def from_json(data: str):
        json_dict = json.loads(data)
        return SensorData(
            json_dict['Ax'],
            json_dict['Az'],
            json_dict['Ay'],
            json_dict['Gx'],
            json_dict['Gy'],
            json_dict['Gz'],
        )

    def get_x_rotation(self):
        radians = math.atan2(self.Ax, dist(self.Ay, self.Az))
        return -math.degrees(radians)

    def get_y_rotation(self):
        radians = math.atan2(self.Ay, dist(self.Ax, self.Az))
        return math.degrees(radians)


def dist(a, b):
    return math.sqrt((a*a)+(b*b))

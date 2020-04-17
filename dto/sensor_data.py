from dataclasses import dataclass
from dataclasses_json import dataclass_json


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
              u'\u00b0' + "/s", "\tAx=%.2f g" % self.Ax, "\tAy=%.2f g" % self.Ay, "\tAz=%.2f g" % self.Az)

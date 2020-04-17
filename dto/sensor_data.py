from dataclasses import dataclass
from dataclasses_json import dataclass_json

# https://pypi.org/project/dataclasses-json/
@dataclass
@dataclass_json
class SensorData:

    Ax: float = 0
    Ay:  float = 0
    Az:  float = 0

    Gx: float = 0
    Gy:  float = 0
    Gz:  float = 0
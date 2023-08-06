import abc
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Extra
from typing_extensions import Literal


class DegreeSchema(str, Enum):
    celsius = "celsius"
    fahrenheit = "fahrenheit"


class DeviceSchema(BaseModel, abc.ABC):
    name: str


class InputDeviceSchema(DeviceSchema, abc.ABC):
    class Config:
        extra = Extra.forbid


class OutputDeviceSchema(DeviceSchema, abc.ABC):
    class Config:
        extra = Extra.forbid


class AM2302Schema(InputDeviceSchema):
    type: Literal["AM2302"]
    degree: Optional[DegreeSchema] = DegreeSchema.celsius
    prefix: Optional[str]
    gpio: int


class SinusSchema(InputDeviceSchema):
    type: Literal["sinus"]
    prefix: Optional[str]


class BME280Schema(InputDeviceSchema):
    type: Literal["bme280"]
    degree: Optional[DegreeSchema] = DegreeSchema.celsius
    prefix: Optional[str]
    gpio: int


class RelaySwitchSchema(OutputDeviceSchema):
    type: Literal["relay"]
    name: str
    gpio: int
    timeout: Optional[int] = 10
    icon: Optional[str]


class DBRelaySwitchSchema(RelaySwitchSchema):
    type: Literal["dbrelay"]

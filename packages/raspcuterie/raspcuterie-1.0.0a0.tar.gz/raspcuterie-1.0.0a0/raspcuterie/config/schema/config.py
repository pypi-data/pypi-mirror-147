from typing import Dict, List, Union, Optional

from pydantic import BaseModel, Extra, Field
from pydantic.fields import Annotated

from .charts import ChartSchema
from .control import ControlGroupSchema
from .devices import (
    AM2302Schema,
    BME280Schema,
    DBRelaySwitchSchema,
    RelaySwitchSchema,
    SinusSchema,
)

DevicesUnion = Annotated[
    Union[
        RelaySwitchSchema,
        DBRelaySwitchSchema,
        AM2302Schema,
        BME280Schema,
        SinusSchema,
    ],
    Field(discriminator="type"),
]


class RaspcuterieConfigSchema(BaseModel):
    name: str
    password: Optional[str]
    devices: List[DevicesUnion]

    control: Dict[str, ControlGroupSchema]
    charts: Dict[str, ChartSchema]

    class Config:
        extra = Extra.allow

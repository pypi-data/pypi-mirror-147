from typing import List

from pydantic import BaseModel, Extra


class ChartSchema(BaseModel):
    title: str
    series: List[str]

    class Config:
        extra = Extra.forbid

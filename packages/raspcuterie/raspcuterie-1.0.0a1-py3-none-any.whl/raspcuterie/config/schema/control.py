from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Extra


class ControleRuleSchema(BaseModel):
    rule: str
    expression: str
    action: str

    class Config:
        extra = Extra.forbid


class ControlGroupSchema(BaseModel):
    expires: Optional[datetime]
    rules: Dict[str, List[ControleRuleSchema]]

    class Config:
        extra = Extra.forbid

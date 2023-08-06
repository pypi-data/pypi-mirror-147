import math
from datetime import datetime
from typing import List

from flask import current_app

from raspcuterie.devices import InputDevice, OutputDevice


class ControlRule:
    registry: List["ControlRule"] = []

    def __init__(
        self, device: OutputDevice, expression: str, action: str, name: str = None
    ):
        ControlRule.registry.append(self)
        self.name = name
        self.device: OutputDevice = device
        self.expression: str = expression
        self.action: str = action

    @staticmethod
    def context():
        context = {"date": datetime.now(), "math": math}

        for device in InputDevice.registry.values():
            for key, value in device.get_context().items():
                if key in context:
                    if hasattr(device, "table_prefix") and device.table_prefix:
                        context[device.table_prefix + "" + key] = value
                    elif hasattr(device, "pin") and device.pin:
                        context[str(device.pin) + "" + key] = value
                    else:
                        print(f"Duplicated key {key} in context")
                else:
                    context[key] = value
        return context

    def matches(self, context):
        return eval(self.expression, context)

    def execute(self):
        try:
            action = getattr(self.device, self.action)
            return action()
        except Exception as e:
            current_app.logger.exception(e)

    def execute_if_matches(self, context):
        if self.matches(context):
            current_app.logger.info(
                f"Matches expression {self.expression}, executing {self.name}.{self.action}"
            )
            return self.execute()
        else:
            current_app.logger.info(f"Does not match expression: {self.expression}")

import logging
from datetime import datetime
from logging import Logger
from pathlib import Path
from typing import Dict, Optional, Tuple

import yaml

from raspcuterie import base_path
from raspcuterie.config.schema import ControlGroupSchema, RaspcuterieConfigSchema
from raspcuterie.devices import InputDevice
from raspcuterie.devices.control import ControlRule
from raspcuterie.devices.output.relay import OutputDevice


def read_config_as_yaml(file: Path) -> Dict:
    InputDevice.discover()
    OutputDevice.discover()

    data = file.read_text()

    data_loaded = yaml.safe_load(data)
    data_loaded["raw"] = data
    return data_loaded


def register_input_devices(config: RaspcuterieConfigSchema, logger: Logger):
    for device in config.devices:
        if device.type in InputDevice.types:
            device_class = InputDevice.types[device.type]
        elif device.type in OutputDevice.types:
            device_class = OutputDevice.types[device.type]
        else:
            device_class = None

        if not device_class:
            logger.error(f"Cloud not initiate {device}")
        else:
            kwargs = device.dict()
            del kwargs["type"]
            del kwargs["name"]

            device_class(device.name, **kwargs)


def register_control_rules(config: RaspcuterieConfigSchema, logger: Logger):
    control_rules: Dict[str, ControlGroupSchema] = config.control

    name, active_control_group = find_active_control_group(control_rules)

    logger.info(
        f"Using control group {name} and will expire {active_control_group.expires}"
    )

    register_control_rules_for_group(active_control_group)


def register_control_rules_for_group(control_group: ControlGroupSchema):
    for device_name, rules in control_group.rules.items():

        device = OutputDevice.registry[device_name]
        for rule in rules:
            ControlRule(
                device,
                expression=rule.expression,
                action=rule.action,
                name=rule.rule,
            )


def find_active_control_group(
    control_groups: Dict[str, ControlGroupSchema]
) -> Optional[Tuple[str, ControlGroupSchema]]:
    """ "
    Finds the group that expires first or the group called default
    """
    active_control_group: Optional[ControlGroupSchema] = None
    active_control_group_name = None

    for key, value in control_groups.items():

        # shortcut
        if len(control_groups) == 1:
            return key, value

        # we have an expiry date in the future
        if value.expires is not None and value.expires > datetime.now():
            if active_control_group is None:
                active_control_group = value
                active_control_group_name = key
            elif (
                active_control_group.expires is None
                or value.expires < active_control_group.expires
            ):
                active_control_group = value

                active_control_group_name = key
        elif value.expires is None and active_control_group is None:

            active_control_group = value

            active_control_group_name = key

    if active_control_group is None:
        return None

    return active_control_group_name, active_control_group


def get_config_file(app) -> Path:
    if app.debug or app.testing:
        file = Path(__file__).parent.parent.parent / "config_dev.yaml"
    else:

        file = base_path / "config.yaml"

    return file


def setup(app):

    if app.debug or app.testing:
        app.logger.setLevel(logging.DEBUG)

    file = get_config_file(app)
    config = read_config_as_yaml(file)

    app.logger.info(f"Loading config {file}")

    RaspcuterieConfigSchema.update_forward_refs()

    app.schema = RaspcuterieConfigSchema.parse_obj(config)
    app.config["config"] = config["raw"]

    register_input_devices(app.schema, app.logger)
    register_control_rules(app.schema, app.logger)

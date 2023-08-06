from pathlib import Path

from raspcuterie.config.setup import (
    read_config_as_yaml,
    register_control_rules,
    register_input_devices,
)
from raspcuterie.config.schema import RaspcuterieConfigSchema
from raspcuterie.devices import InputDevice
from raspcuterie.devices.control import ControlRule
from raspcuterie.devices.output.relay import OutputDevice


def test_parse_config(app):
    file = Path(__file__).parent.parent.parent.parent / "config_dev.yaml"

    ControlRule.registry = []

    x = read_config_as_yaml(file)

    config_object = RaspcuterieConfigSchema.parse_obj(x)

    assert config_object

    register_input_devices(config_object, app.logger)

    assert len(InputDevice.registry) == 3

    assert len(OutputDevice.registry) == 5

    register_control_rules(config_object, app.logger)

    assert len(ControlRule.registry) == 4

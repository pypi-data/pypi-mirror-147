from pathlib import Path

import yaml

from raspcuterie.config import schema


def test_schema():

    x = schema.RaspcuterieConfigSchema.schema()

    assert x

    file = Path(__file__).parent / "config.yaml"

    data = yaml.safe_load(file.read_text())

    settings = schema.RaspcuterieConfigSchema.parse_obj(data)

    assert len(settings.devices) == 6

    assert isinstance(settings.devices[0], schema.RelaySwitchSchema)
    assert isinstance(settings.devices[1], schema.RelaySwitchSchema)
    assert isinstance(settings.devices[2], schema.RelaySwitchSchema)
    assert isinstance(settings.devices[3], schema.RelaySwitchSchema)

    assert isinstance(settings.devices[4], schema.AM2302Schema)
    assert settings.devices[4].degree == schema.DegreeSchema.celsius

    assert isinstance(settings.devices[5], schema.SinusSchema)

    assert "default" in settings.control

    default_control = settings.control.get("default")

    assert len(default_control.rules.keys()) == 2

    assert default_control.expires.year == 2020


def test_jsonschema():

    jsonschema = schema.RaspcuterieConfigSchema.schema_json()

    print(jsonschema)

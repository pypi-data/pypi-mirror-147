import pytest

from raspcuterie.devices import OutputDevice
from raspcuterie.devices.control import ControlRule
from raspcuterie.devices.input.am2302 import AM2302
from raspcuterie.devices.output.relay import DBRelay


@pytest.mark.parametrize("temperature,match", [(11, True), (9, False)])
def test_matches(temperature, match):

    AM2302("am2303")

    relay = DBRelay("test")

    x = ControlRule(device=relay, expression="temperature >= 10", action="on")

    assert x.matches(dict(temperature=temperature)) == match


def test_execute(monkeypatch, app):

    with app.app_context():

        monkeypatch.setattr(AM2302, "read", lambda: (0, 7))

        relay = DBRelay("test")

        assert "test" in OutputDevice.registry

        x = ControlRule(device=relay, expression="True", action="on")
        x.execute()

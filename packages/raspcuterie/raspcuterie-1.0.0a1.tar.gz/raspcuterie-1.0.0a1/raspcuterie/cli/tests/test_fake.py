from raspcuterie.cli import fake
from raspcuterie.db import get_db
from raspcuterie.devices import InputDevice
from raspcuterie.devices.input.am2302 import AM2302


def test_fake_humidity(runner, app):

    with app.app_context():
        device: AM2302 = InputDevice.registry["temperature"]

        device.h_series.create_table(get_db())

        result = runner.invoke(
            fake.humidity, device.h_series.name, catch_exceptions=False
        )
        assert result.exit_code == 0, result.exception

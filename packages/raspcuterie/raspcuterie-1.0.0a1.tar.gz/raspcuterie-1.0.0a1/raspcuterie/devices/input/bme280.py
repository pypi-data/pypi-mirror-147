from flask import current_app

from raspcuterie.devices import InputDevice, LogDevice
from raspcuterie.devices.series import HumiditySeries, TemperatureSeries
from raspcuterie.utils import min_max_avg_over_period


class BME280(InputDevice, LogDevice):
    type = "bme280"

    DEGREE_CELSIUS = "celsius"
    DEGREE_FAHRENHEIT = "fahrenheit"

    table_sql = """
        create table if not exists {0}
        (
            id    integer primary key,
            time  text not null,
            value integer not null
        );"""

    def __init__(self, name, degree=DEGREE_CELSIUS, prefix="", **kwargs):
        super().__init__(name)
        self.port = 1
        self.address = 0x76
        self.degree = degree
        self.prefix = prefix

        self.h_series = HumiditySeries(f"{prefix}_humidity")
        self.t_series = TemperatureSeries(f"{prefix}_temperature")

    def read(self):
        humidity, temperature = self.raw()

        if humidity:
            humidity = round(humidity, 1)

        if temperature:
            temperature = round(temperature, 1)

        return humidity, temperature

    def raw(self):
        import bme280
        from smbus2 import smbus2

        port = 1
        address = 0x76
        bus = smbus2.SMBus(port)

        calibration_params = bme280.load_calibration_params(bus, address)

        # the sample method will take a single reading and return a
        # compensated_reading object
        sensor = bme280.sample(bus, address, calibration_params)

        # the compensated_reading class has the following attributes

        try:
            temperature = sensor.temperature
            humidity = sensor.humidity
        except RuntimeError as e:
            current_app.logger.error(e)
            temperature = None
            humidity = None

        if self.degree != "celsius" and temperature:
            temperature = temperature * 9 / 5 + 32

        return humidity, temperature

    def get_context(self):

        humidity, temperature = self.read()

        humidity_min_3h, humidity_max_3h, humidity_avg_3h = min_max_avg_over_period(
            self.h_series.name, "-3 hours"
        )

        values = dict(
            humidity=humidity,
            temperature=temperature,
            humidity_min_3h=humidity_min_3h,
            humidity_max_3h=humidity_max_3h,
            humidity_avg_3h=humidity_avg_3h,
        )

        values[self.t_series.name] = temperature
        values[self.h_series.name] = humidity

        return values

    def log(self):

        humidity, temperature = self.read()

        self.h_series.log(humidity)
        self.t_series.log(temperature)

from flask import current_app, g

from raspcuterie.devices import InputDevice, LogDevice
from raspcuterie.devices.series import HumiditySeries, TemperatureSeries
from raspcuterie.utils import min_max_avg_over_period


class HumidityTemperatureDevice(InputDevice, LogDevice):
    pass


class AM2302(HumidityTemperatureDevice):
    type = "AM2302"

    DEGREE_CELSIUS = "celsius"
    DEGREE_FAHRENHEIT = "fahrenheit"

    def __init__(self, name, degree=DEGREE_CELSIUS, gpio=4, prefix=""):
        super(AM2302, self).__init__(name)
        self.pin = gpio
        self.degree = degree
        self.prefix = prefix

        self.h_series = HumiditySeries(f"{prefix}_humidity")
        self.t_series = TemperatureSeries(f"{prefix}_temperature")

    @staticmethod
    def get_sensor(gpio_pin):
        sensor = f"am2302_{gpio_pin}"
        if sensor not in g:

            from adafruit_dht import DHT22  # noqa
            from board import pin

            gpio_pin = pin.Pin(gpio_pin)

            setattr(g, sensor, DHT22(gpio_pin))

        return getattr(g, sensor)

    def read(self):
        humidity, temperature = self.raw()

        if humidity:
            humidity = round(humidity, 1)

        if temperature:
            temperature = round(temperature, 1)

        return humidity, temperature

    def raw(self):
        sensor = AM2302.get_sensor(self.pin)

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

    def temperature_data(self, period="-24 hours", aggregate=5 * 60):
        return self.t_series.data(period, aggregate)

    def humidity_data(self, period="-24 hours", aggregate=5 * 60):
        return self.h_series.data(period, aggregate)

    def log(self):

        humidity, temperature = self.read()

        self.h_series.log(humidity)
        self.t_series.log(temperature)

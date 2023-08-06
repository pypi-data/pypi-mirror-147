import datetime
from builtins import super

from flask import current_app

from raspcuterie.db import get_db
from raspcuterie.devices import LogDevice, OutputDevice
from raspcuterie.devices.series import BooleanSeries
from raspcuterie.gpio import GPIO

ICON_PRESETS = {
    "refrigerator": "fa-refrigerator",
    "heater": "fa-heat",
    "humidifier": "fa-shower",
    "dehumidifier": "fa-air-conditioner",
    "fan": "fa-fan",
}


class RelaySwitch(OutputDevice, LogDevice):
    type = "relay"

    def __init__(self, name, gpio, timeout=10, icon=""):
        super(RelaySwitch, self).__init__(name)

        self.pin_number = gpio
        self.timeout_minutes = timeout
        if gpio:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin_number, GPIO.OUT)
        self._icon = icon
        self.series = BooleanSeries(self.name)

    @property
    def icon(self):
        if self._icon:
            return self._icon

        name_lower = self.name.lower()

        return ICON_PRESETS.get(name_lower, "")

    def last_db_value(self):

        with get_db() as db:

            cursor = db.execute(
                """SELECT time, value FROM {} ORDER BY time DESC LIMIT 1""".format(
                    self.series.name
                )
            )

            return cursor.fetchone()

    def validate_timeout(self):

        result = self.last_db_value()

        if result and result[0]:
            before = datetime.datetime.now() - datetime.timedelta(
                minutes=self.timeout_minutes
            )
            last_seen = datetime.datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S.%f")
            current_app.logger.debug(f"{self.name} is last seen on {last_seen}")
            return last_seen < before

        return True

    def _set_output(self, value):
        GPIO.output(self.pin_number, value)

    def _set_value(self, value):
        if self.validate_timeout():
            self._set_output(value)
            self.update_table(self.value())
            return True
        else:
            current_app.logger.debug("Timeout for relay")
            return False

    def on(self):
        self._set_value(GPIO.HIGH)

    def off(self):
        return self._set_value(GPIO.LOW)

    def value(self):
        return GPIO.input(self.pin_number)

    def chart(self, period="-24 hours"):
        cursor = get_db().execute(
            """SELECT time, value
FROM {0} t
WHERE t.value is not null
  and time >= datetime('now', :period)
ORDER BY time DESC;""".format(
                self.table_name
            ),
            dict(period=period),
        )

        r = cursor.fetchall()
        x = []
        previous_time = None
        for time, value in r:
            if not previous_time:
                previous_time = time
            else:
                x.append((previous_time, value))
                previous_time = time

        if len(x) > 0:
            # close the gap by extending the last value to now
            first = x[0]

            x = [(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), first[1])] + x

        return x

    def update_table(self, value, time=None):

        last_value = self.last_db_value()

        if last_value and value == last_value[1]:
            current_app.logger.debug(
                f"No change in value ({value}) for relay {self.name}"
            )
            return

        if not time:
            time = datetime.datetime.now()

        db = get_db()

        with db:
            db.execute(
                "INSERT INTO {0}(time,value) VALUES (?,?)".format(self.table_name),
                (time, value),
            )

    @property
    def table_name(self):
        return self.series.name


class DBRelay(RelaySwitch, LogDevice):
    type = "dbrelay"

    def __init__(self, name, gpio=0, timeout=10, icon="fa-close"):
        super(DBRelay, self).__init__(name, gpio=gpio, timeout=timeout, icon=icon)

    def _set_output(self, value):
        self.update_table(value == GPIO.HIGH)

    @property
    def table_name(self):
        return self.series.name

    def value(self):
        cursor = get_db().execute(
            "SELECT value FROM {0} ORDER BY time DESC LIMIT 1".format(self.series.name)
        )

        row = cursor.fetchone()

        if row:
            return bool(row[0])

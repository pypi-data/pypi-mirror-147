"""
HX711 Load cell amplifier Python Library
Original source: https://gist.github.com/underdoeg/98a38b54f889fce2b237
Documentation source: https://github.com/aguegu/ardulibs/tree/master/hx711
Adapted by 2017 Jiri Dohnalek

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
import statistics

from flask import g

# import hx711

from raspcuterie.db import insert_weight, get_db
from raspcuterie.devices import InputDevice, DatabaseDevice, LogDevice


class HX711(InputDevice, DatabaseDevice, LogDevice):
    def __init__(
        self, name, dout=12, pd_sck=16, gain=128, channel="A", offset=0, scale=1
    ):
        super(HX711, self).__init__(name)
        """
        Set GPIO Mode, and pin for communication with HX711
        :param dout: Serial Data Output pin
        :param pd_sck: Power Down and Serial Clock Input pin
        :param gain: set gain 128, 64, 32
        """

        self.dout = dout
        self.pd_sck = pd_sck
        self.offset = offset
        self.scale = scale
        self.channel = channel
        self.gain = gain

    def read(self):
        raw = self.sensor.get_raw_data(32)

        raw.sort()

        # drop highest and lowest
        raw = raw[1:-1]

        mean = statistics.mean(raw)
        st_dev = statistics.stdev(raw, mean)

        error = st_dev * 2

        lower = mean - error
        upper = mean + error

        filtered = [x for x in raw if lower < x < upper]

        if len(filtered) == 0:
            print(raw)
            print(mean)
            print(st_dev)
            return None

        return statistics.mean(filtered)

    @property
    def sensor(self):
        return HX711.get_sensor(self.dout, self.pd_sck, self.gain, self.channel)

    @staticmethod
    def get_sensor(dout_pin, pd_sck_pin, gain, channel):

        if "hx711" not in g:
            g.hx711 = hx711.HX711(dout_pin, pd_sck_pin, gain, channel)

        return g.hx711

    def get_grams(self):
        """
        :param times: Set value to calculate average,
        be aware that high number of times will have a
        slower runtime speed.
        :return float weight in grams
        """
        raw = self.read()
        value = raw - self.offset
        grams = value / self.scale
        return grams

    def get_context(self):
        return dict()

    def log(self):
        grams = self.get_grams()

        insert_weight(grams)

    def create_table(self, connection):
        connection.execute(self.single_value_table_sql.format("weight"))

    def weight_data(self, period="-24 hours", aggregate=5 * 60):

        cursor = get_db().execute(
            """SELECT datetime(strftime('%s', t.time) - (strftime('%s', t.time) % :aggregate), 'unixepoch') time,
       round(avg(value), 2)                                                                value
FROM weight t
WHERE t.value is not null
  and time >= datetime('now', :period)
GROUP BY strftime('%s', t.time) / :aggregate
ORDER BY time DESC;""",
            dict(period=period, aggregate=aggregate),
        )

        temperature_data = cursor.fetchall()
        cursor.close()
        return temperature_data

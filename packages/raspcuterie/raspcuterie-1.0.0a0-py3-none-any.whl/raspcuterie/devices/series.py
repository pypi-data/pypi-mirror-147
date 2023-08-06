from datetime import datetime
from typing import Dict

from flask import current_app

from raspcuterie.db import get_db
from raspcuterie.utils import min_max_avg_over_period, slope


class Series:
    type: str
    registry: Dict[str, "Series"] = {}

    table_sql = """
            create table if not exists {0}
            (
                id    integer primary key,
                time  text not null,
                value integer not null
            );"""

    def __init__(self, name):
        self.name = name
        Series.registry[name] = self

    def create_table(self, connection):
        connection.execute(self.table_sql.format(self.name))

    def log(self, value, time_value=None):

        if value is None:
            current_app.logger.info(f"Received None for {self.name}, discarding value.")
            return

        if time_value is None:
            time_value = datetime.now()

        db = get_db()

        with db:
            db.execute(
                f"INSERT INTO {self.name}(time,value) VALUES (?,?)",
                (time_value, value),
            )

    def data(self, period="-24 hours", aggregate=5 * 60):
        table_name = self.name
        cursor = get_db().execute(
            f"""SELECT datetime(strftime('%s', t.time) - (strftime('%s', t.time) % :aggregate), 'unixepoch') time,
               round(avg(value), 2)                                                                value
        FROM {table_name} t
        WHERE t.value is not null
          and time >= datetime('now', :period)
        GROUP BY strftime('%s', t.time) / :aggregate
        ORDER BY time DESC;""",
            dict(period=period, aggregate=aggregate),
        )

        data = cursor.fetchall()

        cursor.close()

        return data

    def last_observation(self, period="-24 hours"):
        time = None

        table_name = self.name

        observation = (
            get_db()
            .execute(f"SELECT value, time FROM {table_name} ORDER BY time DESC LIMIT 1")
            .fetchone()
        )

        if observation:
            time = observation[1]
            observation = observation[0]

        series_slope = slope(self.name)

        min, max, avg = min_max_avg_over_period(self.name, period)

        temperature = dict(
            current=observation,
            min=round(min, 2),
            max=round(max, 2),
            avg=round(avg, 2),
            slope=series_slope,
        )

        return time, temperature


class IntegerSeries(Series):
    min: int
    max: int
    type = "integer"

    def last_observation(self, period="-24 hours"):
        time = None

        table_name = self.name

        observation = (
            get_db()
            .execute(f"SELECT value, time FROM {table_name} ORDER BY time DESC LIMIT 1")
            .fetchone()
        )

        if observation:
            time = observation[1]
            observation = observation[0]

        series_slope = slope(self.name)

        min, max, avg = min_max_avg_over_period(self.name, period)

        data = dict(
            current=observation,
            min=round(min, 2),
            max=round(max, 2),
            avg=round(avg, 2),
            slope=series_slope,
        )

        return time, data


class HumiditySeries(IntegerSeries):
    min = 40
    max = 85


class TemperatureSeries(IntegerSeries):
    min = 5
    max = 30


class BooleanSeries(Series):
    type = "boolean"

    table_sql = """
    create table if not exists {0}
    (
        id    integer primary key,
        time  text not null,
        value integer not null
    );"""

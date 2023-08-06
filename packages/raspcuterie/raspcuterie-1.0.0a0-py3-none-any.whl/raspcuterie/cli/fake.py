import datetime
import random
from typing import List

import click
from flask.cli import with_appcontext

from raspcuterie import db, utils
from raspcuterie.cli import cli
from raspcuterie.devices.series import Series


def date_generator(start, stop, **interval):
    while start < stop:
        yield start
        start += datetime.timedelta(**interval)


@cli.group()
def fake():
    """Fake values for your sensors"""


@fake.command(short_help="Fake temperature series")
@click.argument("table")
@with_appcontext
def temperature(table):
    insert_single_value_data(db.insert_temperature, table, 5, 25, 60)


@fake.command(short_help="Fake humidity series")
@click.argument("table")
@with_appcontext
def humidity(table):
    insert_single_value_data(db.insert_humidity, table, 60, 95)


@fake.command()
@click.argument("table")
@with_appcontext
def weight(table):
    insert_single_value_data(db.insert_weight, table, 300, 150)


@fake.command()
@click.argument("table")
@with_appcontext
def relay(table):
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(hours=24)
    x: List[datetime.datetime] = list(date_generator(yesterday, today, minutes=10))

    with click.progressbar(x) as bar:
        for date in bar:

            series = Series(table)

            series.log(bool(random.getrandbits(1)), date)


def insert_single_value_data(db_function, table: str, lower, upper, minutes_extra=0):
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(hours=24)
    x: List[datetime.datetime] = list(date_generator(yesterday, today, minutes=1))

    with click.progressbar(x) as bar:
        for date in bar:

            z = date + datetime.timedelta(minutes=minutes_extra)

            minute = z.minute + (z.hour % 6 * 60) + minutes_extra

            db_function(table, utils.time_based_sinus(minute, lower, upper, 1), date)

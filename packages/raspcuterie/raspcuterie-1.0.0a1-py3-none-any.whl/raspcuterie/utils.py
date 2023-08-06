import math

from raspcuterie.db import get_db


def time_based_sinus(minute, lower, upper, multiplier=6):
    delta = upper - lower
    middle = lower + delta / 2

    return round(middle + math.sin(math.radians(minute * multiplier)) * (delta / 2), 2)


def gettext(value: str):
    return value


def slope(table):
    x_series = range(1, 6)
    x_average = sum(x_series) / 5

    series = get_db().execute(
        "SELECT value FROM {} ORDER BY time DESC LIMIT 5".format(table)
    )

    y_series = list(reversed([x[0] for x in series.fetchall()]))

    y_average = sum(y_series) / 5

    average_delta = sum(
        [(x - x_average) * (y - y_average) for x, y in zip(x_series, y_series)]
    )

    # we have a series of 5
    x_constant = 10

    return round(average_delta / x_constant, 2)


def min_max_avg_over_period(table: str, period="-24 hours"):
    result = get_db().execute(
        """SELECT min(value), max(value), avg(value)
FROM {} as t
WHERE t.value is not null
  and t.time >= datetime('now', :period)""".format(
            table
        ),
        dict(period=period),
    )
    min_value, max_value, avg_value = result.fetchone()

    if not min_value:
        min_value = 0

    if not max_value:
        max_value = 0

    if not avg_value:
        avg_value = 0

    return min_value, max_value, avg_value

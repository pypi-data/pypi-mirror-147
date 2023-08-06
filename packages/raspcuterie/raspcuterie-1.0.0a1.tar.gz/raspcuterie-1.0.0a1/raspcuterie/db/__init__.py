import sqlite3
from datetime import datetime

from flask import current_app, g


def raw_connection(app):

    return sqlite3.connect(
        app.config["DATABASE"],
        detect_types=sqlite3.PARSE_DECLTYPES,
        check_same_thread=False,
    )


def get_db():
    if "db" not in g:
        g.db = raw_connection(current_app)
        # g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db(connection=None):

    if not connection:
        connection = get_db()

    from raspcuterie.devices.series import Series

    for series in Series.registry.values():
        series.create_table(connection)


def insert_temperature(table_name, value: float, time_value=None):

    if time_value is None:
        time_value = datetime.now()

    previous_value = (
        get_db()
        .execute(f"SELECT value FROM {table_name} ORDER BY time DESC LIMIT 1")
        .fetchone()
    )

    if previous_value and round(previous_value[0], 1) == round(value, 1):
        current_app.logger.info("Temperature: no significant change")
    else:
        current_app.logger.info(f"Temperature: logging {value} ")
        db = get_db()

        with db:
            db.execute(
                f"INSERT INTO {table_name}(time,value) VALUES (?,?)",
                (time_value, value),
            )


def insert_humidity(table_name, value: float, time_value=None):

    if time_value is None:
        time_value = datetime.now()

    previous_value = (
        get_db()
        .execute(f"SELECT value FROM {table_name} ORDER BY time DESC LIMIT 1")
        .fetchone()
    )

    if previous_value and round(previous_value[0], 1) == round(value, 1):
        current_app.logger.info("Humidity: no significant change")
    else:
        current_app.logger.info(f"Humidity: logging {value} ")
        db = get_db()

        with db:
            db.execute(
                f"INSERT INTO {table_name}(time,value) VALUES (?,?)",
                (time_value, value),
            )


def insert_relay(table: str, value_1, value_2, value_3, value_4):
    db = get_db()
    with db:
        db.execute(
            f"INSERT INTO {table}(time,value_1, value_2, value_3, value_4) VALUES (?, ?, ?, ?, ?)",
            (datetime.now(), value_1, value_2, value_3, value_4),
        )


def insert_weight(table: str, value: float, time_value=None):

    if time_value is None:
        time_value = datetime.now()

    db = get_db()

    with db:
        current_app.logger.info(f"Weight: logging {value} ")
        db.execute(f"INSERT INTO {table}(time,value) VALUES (?,?)", (time_value, value))

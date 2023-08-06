from raspcuterie.db import get_db
from raspcuterie.devices.output.relay import DBRelay


def test_on(app):

    with app.app_context():
        x = DBRelay("test")
        x.create_table(get_db())
        x.on()

        assert x.value() is True


def test_off(app):

    with app.app_context():
        x = DBRelay("test")

        x.off()

        assert x.value() is False


def _count(x):
    with get_db() as db:
        cursor = db.execute(f"SELECT COUNT(*) FROM {x.table_name}")
        return cursor.fetchone()[0]


def test_update_table(app):

    with app.app_context():
        x = DBRelay("test")
        x.create_table(get_db())
        x.on()

        assert x.value() is True

        assert _count(x) == 1

        x.update_table(x.value())

        assert _count(x) == 1

        x.update_table(not x.value())

        assert _count(x) == 2

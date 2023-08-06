import os

from flask import Flask, g
from flask_babel import Babel

from raspcuterie import base_path, version
from raspcuterie.config import setup
from raspcuterie.dashboard import api, dashboard
from raspcuterie.db import close_db, init_db, raw_connection
from raspcuterie.utils import gettext

Babel()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True, template_folder="./templates")

    app.config.from_mapping(
        DATABASE=os.environ.get("DATABASE", str(base_path / "raspcuterie.db"))
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(api.bp)
    app.register_blueprint(dashboard.bp)

    app.teardown_appcontext(close_db)
    app.teardown_appcontext(close_pulseio)

    setup(app)
    init_db(raw_connection(app))

    app.jinja_env.globals["version"] = version
    app.jinja_env.globals["gettext"] = gettext
    return app


def close_pulseio(e=None):
    sensor = g.pop("am2302", None)

    if sensor:
        sensor.exit()

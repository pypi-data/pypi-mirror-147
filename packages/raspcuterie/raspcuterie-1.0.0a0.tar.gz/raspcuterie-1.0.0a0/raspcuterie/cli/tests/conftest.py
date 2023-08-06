import pytest


@pytest.fixture
def runner(app):
    app.config["TESTING"] = True
    return app.test_cli_runner()

import pytest
from api import create_app
from flask_migrate import upgrade


@pytest.fixture()
def app():
    app = create_app("test")
    with app.app_context():
        upgrade()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

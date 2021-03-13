import pytest

from app import create_app, db
from config import Config

# pylint: disable=redefined-outer-name
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


@pytest.fixture
def app():
    yield create_app(TestConfig)


@pytest.fixture
def client(app):
    with app.app_context():
        db.create_all()
        yield app.test_client()

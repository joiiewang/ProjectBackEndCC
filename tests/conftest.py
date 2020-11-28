import pytest

from myapp import app as flask_app
from database import db

@pytest.fixture
def app():
    with flask_app.app_context():
        # Resetting database
        db.drop_all()
        db.create_all()
    yield flask_app

@pytest.fixture
def client(app):
        return app.test_client()

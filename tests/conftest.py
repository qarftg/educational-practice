import pytest
from server.app import app, db

@pytest.fixture(scope='module')
def test_app():
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres@localhost/test_db',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    yield app

@pytest.fixture(scope='module')
def test_client(test_app):
    with test_app.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def init_db(test_app):
    with test_app.app_context():
        db.create_all()
        yield db

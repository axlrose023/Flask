import pytest
from app import app


@pytest.fixture(scope='session')
def app():
    params = {
        'DEBUG': False,
        'TESTING': True,
    }

    _app = app(settings_override=params)
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def client(app):
    yield app.test_client()

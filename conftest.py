import pytest
from app import *
from create_app import *
import requests_mock

@pytest.fixture(scope='session')
def app():
    # Create and configure the app for the test
    app = create_app()
    app.config['TESTING'] = True

    # Perform additional configurations if needed

    yield app

@pytest.fixture(scope='session')
def client(app):
    # Create a test client
    with app.test_client() as client:
        yield client



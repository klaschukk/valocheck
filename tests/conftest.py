import pytest

from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["BASE_URL"] = "http://localhost:5001"
    yield app


@pytest.fixture
def client(app):
    return app.test_client()

import pytest
from app import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

    print(response.json)
    print(response.text)
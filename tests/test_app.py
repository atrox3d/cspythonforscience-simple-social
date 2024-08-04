import pytest
from app import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

def test_static_home(client):
    response = client.get('/')
    assert response.status_code == 200
    print(response.text)
    assert '<h1>simple social</h1>' in response.text

    with open('templates/index.html') as fp:
        html = fp.read()
    assert response.text == html

import pytest
from backend.app import create_app

@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_app_startup(client):
    response = client.get('/api/status')
    assert response.status_code == 200
    assert response.json == {"status": "ok", "message": "Health Connect API is running"}

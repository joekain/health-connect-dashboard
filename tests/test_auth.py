import pytest
from flask import jsonify
from backend.app import create_app

@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_get_token_valid_credentials(client):
    response = client.post('/api/auth/token', json={'password': 'your_secure_password'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert 'expires' in data

def test_get_token_invalid_credentials(client):
    response = client.post('/api/auth/token', json={'password': 'wrong_password'})
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid credentials'

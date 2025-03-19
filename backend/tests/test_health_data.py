import pytest
from backend.app import create_app
from backend.app.models.weight import WeightRecord
from backend.app.models.body_fat import BodyFatRecord
from backend.app.models.calories import CaloriesRecord
from backend.app.models.nutrition import NutritionRecord
from datetime import datetime

@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_sync_weight_data(client):
    response = client.post('/api/health_data/sync', json={
        'weightData': [
            {'timestamp': datetime.utcnow().isoformat(), 'weight': 70.5}
        ]
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'

def test_sync_body_fat_data(client):
    response = client.post('/api/health_data/sync', json={
        'bodyFatData': [
            {'timestamp': datetime.utcnow().isoformat(), 'percentage': 15.0}
        ]
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'

def test_sync_calories_data(client):
    response = client.post('/api/health_data/sync', json={
        'caloriesData': [
            {'timestamp': datetime.utcnow().isoformat(), 'total_calories': 2000}
        ]
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'

def test_sync_nutrition_data(client):
    response = client.post('/api/health_data/sync', json={
        'nutritionData': [
            {'timestamp': datetime.utcnow().isoformat(), 'calories': 500}
        ]
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'

def test_get_weight_data(client):
    response = client.get('/api/health_data/weight')
    assert response.status_code == 200

def test_get_body_fat_data(client):
    response = client.get('/api/health_data/body-fat')
    assert response.status_code == 200

def test_get_calories_data(client):
    response = client.get('/api/health_data/calories')
    assert response.status_code == 200

def test_get_nutrition_data(client):
    response = client.get('/api/health_data/nutrition')
    assert response.status_code == 200

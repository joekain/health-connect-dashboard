import unittest
import json
from app import create_app, db
from app.models.weight import WeightRecord
from app.models.body_fat import BodyFatRecord
from app.models.calories import CaloriesRecord
from app.models.nutrition import NutritionRecord

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({'TESTING': True})
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def get_auth_token(self):
        response = self.client.post('/api/auth/token', json={'password': 'your_secure_password'})
        data = json.loads(response.data)
        return data['token']

    def test_status_endpoint(self):
        response = self.client.get('/api/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'ok')

    def test_sync_weight_data(self):
        token = self.get_auth_token()
        headers = {'Authorization': f'Bearer {token}'}
        data = {
            'weightData': [
                {'timestamp': '2023-01-01T00:00:00', 'weight': 70.5}
            ]
        }
        response = self.client.post('/api/sync', json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')

        with self.app.app_context():
            records = WeightRecord.query.all()
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].weight_kg, 70.5)

    def test_sync_invalid_weight_data(self):
        token = self.get_auth_token()
        headers = {'Authorization': f'Bearer {token}'}
        data = {
            'weightData': [
                {'timestamp': 'invalid-timestamp', 'weight': 70.5}
            ]
        }
        response = self.client.post('/api/sync', json=data, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['status'], 'error')

    def test_sync_body_fat_data(self):
        token = self.get_auth_token()
        headers = {'Authorization': f'Bearer {token}'}
        data = {
            'bodyFatData': [
                {'timestamp': '2023-01-01T00:00:00', 'percentage': 15.5}
            ]
        }
        response = self.client.post('/api/sync', json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')

        with self.app.app_context():
            records = BodyFatRecord.query.all()
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].percentage, 15.5)

    def test_sync_invalid_body_fat_data(self):
        token = self.get_auth_token()
        headers = {'Authorization': f'Bearer {token}'}
        data = {
            'bodyFatData': [
                {'timestamp': 'invalid-timestamp', 'percentage': 15.5}
            ]
        }
        response = self.client.post('/api/sync', json=data, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['status'], 'error')

    def test_sync_calories_data(self):
        token = self.get_auth_token()
        headers = {'Authorization': f'Bearer {token}'}
        data = {
            'caloriesData': [
                {'timestamp': '2023-01-01T00:00:00', 'total_calories': 2000}
            ]
        }
        response = self.client.post('/api/sync', json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')

        with self.app.app_context():
            records = CaloriesRecord.query.all()
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].total_calories, 2000)

    def test_sync_invalid_calories_data(self):
        token = self.get_auth_token()
        headers = {'Authorization': f'Bearer {token}'}
        data = {
            'caloriesData': [
                {'timestamp': 'invalid-timestamp', 'total_calories': 2000}
            ]
        }
        response = self.client.post('/api/sync', json=data, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['status'], 'error')

    def test_sync_nutrition_data(self):
        token = self.get_auth_token()
        headers = {'Authorization': f'Bearer {token}'}
        data = {
            'nutritionData': [
                {'timestamp': '2023-01-01T00:00:00', 'calories': 500, 'protein_grams': 30, 'carbs_grams': 50, 'fat_grams': 20}
            ]
        }
        response = self.client.post('/api/sync', json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')

        with self.app.app_context():
            records = NutritionRecord.query.all()
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].calories, 500)

    def test_sync_invalid_nutrition_data(self):
        token = self.get_auth_token()
        headers = {'Authorization': f'Bearer {token}'}
        data = {
            'nutritionData': [
                {'timestamp': 'invalid-timestamp', 'calories': 500}
            ]
        }
        response = self.client.post('/api/sync', json=data, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['status'], 'error')

    def test_token_authentication(self):
        response = self.client.post('/api/auth/token', json={'password': 'your_secure_password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)

    def test_invalid_token_authentication(self):
        response = self.client.post('/api/auth/token', json={'password': 'wrong_password'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()

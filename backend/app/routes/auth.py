from flask import Blueprint, request, jsonify
import os
import secrets
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

# For MVP, a simple token-based auth is sufficient
API_TOKEN = os.environ.get('API_TOKEN') or secrets.token_hex(16)
print(f"API Token: {API_TOKEN}")  # For development only

@auth_bp.route('/token', methods=['POST'])
def get_token():
    # For MVP, a simple password check is sufficient
    password = request.json.get('password')
    
    # Replace with your preferred authentication method
    if password == 'your_secure_password':
        return jsonify({
            'token': API_TOKEN,
            'expires': (datetime.now() + timedelta(days=30)).isoformat()
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401
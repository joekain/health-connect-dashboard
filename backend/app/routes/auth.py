from flask import Blueprint, request, jsonify, g
import os
import secrets
from datetime import datetime, timedelta
from functools import wraps

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

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != f"Bearer {API_TOKEN}":
            return jsonify({'error': 'Unauthorized access'}), 401
        return f(*args, **kwargs)
    return decorated_function

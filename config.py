import os
from pathlib import Path

# Create data directory if it doesn't exist
data_dir = Path(__file__).parent / 'data'
data_dir.mkdir(exist_ok=True)

class Config:
    # Basic configuration
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    
    # SQLite Database - store in a 'data' subdirectory
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{data_dir}/health_connect.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
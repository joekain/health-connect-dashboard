from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    with app.app_context():
        db.create_all()
        print("Database initialized successfully")

# Import models after db is defined to avoid circular imports
from models.weight import WeightRecord
from models.body_fat import BodyFatRecord
from models.calories import CaloriesRecord
from models.nutrition import NutritionRecord
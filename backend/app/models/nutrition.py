from app import db
from datetime import datetime
import json

class NutritionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Basic nutrition data
    calories = db.Column(db.Float)
    protein_grams = db.Column(db.Float)
    carbs_grams = db.Column(db.Float)
    fat_grams = db.Column(db.Float)
    
    # Meal type (breakfast, lunch, dinner, snack)
    meal_type = db.Column(db.String(20))
    
    # Additional nutrition details stored as JSON
    details = db.Column(db.Text)
    
    source = db.Column(db.String(50))
    
    def set_details(self, details_dict):
        self.details = json.dumps(details_dict)
    
    def get_details(self):
        if self.details:
            return json.loads(self.details)
        return {}
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'calories': self.calories,
            'protein_grams': self.protein_grams,
            'carbs_grams': self.carbs_grams,
            'fat_grams': self.fat_grams,
            'meal_type': self.meal_type,
            'details': self.get_details(),
            'source': self.source
        }
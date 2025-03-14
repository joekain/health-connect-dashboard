from . import db
from datetime import datetime

class CaloriesRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Calories data
    active_calories = db.Column(db.Float)
    basal_calories = db.Column(db.Float)
    total_calories = db.Column(db.Float, nullable=False)
    
    source = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'active_calories': self.active_calories,
            'basal_calories': self.basal_calories,
            'total_calories': self.total_calories,
            'source': self.source
        }
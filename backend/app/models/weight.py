from app import db
from datetime import datetime

class WeightRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    weight_kg = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'weight_kg': self.weight_kg,
            'source': self.source
        }
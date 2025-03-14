from app import db
from datetime import datetime

class BodyFatRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    percentage = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'percentage': self.percentage,
            'source': self.source
        }
from flask import Blueprint, request, jsonify
from app import db
from app.models.weight import WeightRecord
from app.models.body_fat import BodyFatRecord
from app.models.calories import CaloriesRecord
from app.models.nutrition import NutritionRecord
from datetime import datetime, timedelta

health_data_bp = Blueprint('health_data', __name__)

@health_data_bp.route('/sync', methods=['POST'])
def sync_data():
    data = request.json
    
    # Process weight data
    if 'weightData' in data:
        for record in data['weightData']:
            if not validate_weight_data(record):
                return jsonify({"status": "error", "message": "Invalid weight data"}), 400
            weight_entry = WeightRecord(
                user_id='your_user_id',  # For MVP, hardcoded is fine
                timestamp=datetime.fromisoformat(record['timestamp']),
                weight_kg=record['weight'],
                source=record.get('source', 'health_connect')
            )
            db.session.add(weight_entry)
    
    # Process body fat data
    if 'bodyFatData' in data:
        for record in data['bodyFatData']:
            if not validate_body_fat_data(record):
                return jsonify({"status": "error", "message": "Invalid body fat data"}), 400
            body_fat_entry = BodyFatRecord(
                user_id='your_user_id',
                timestamp=datetime.fromisoformat(record['timestamp']),
                percentage=record['percentage'],
                source=record.get('source', 'health_connect')
            )
            db.session.add(body_fat_entry)
            
    # Process calories data
    if 'caloriesData' in data:
        for record in data['caloriesData']:
            if not validate_calories_data(record):
                return jsonify({"status": "error", "message": "Invalid calories data"}), 400
            calories_entry = CaloriesRecord(
                user_id='your_user_id',
                timestamp=datetime.fromisoformat(record['timestamp']),
                active_calories=record.get('active_calories'),
                basal_calories=record.get('basal_calories'),
                total_calories=record['total_calories'],
                source=record.get('source', 'health_connect')
            )
            db.session.add(calories_entry)
    
    # Process nutrition data
    if 'nutritionData' in data:
        for record in data['nutritionData']:
            if not validate_nutrition_data(record):
                return jsonify({"status": "error", "message": "Invalid nutrition data"}), 400
            nutrition_entry = NutritionRecord(
                user_id='your_user_id',
                timestamp=datetime.fromisoformat(record['timestamp']),
                calories=record.get('calories'),
                protein_grams=record.get('protein_grams'),
                carbs_grams=record.get('carbs_grams'),
                fat_grams=record.get('fat_grams'),
                meal_type=record.get('meal_type'),
                source=record.get('source', 'health_connect')
            )
            
            # Handle additional details if present
            if 'details' in record and record['details']:
                nutrition_entry.set_details(record['details'])
                
            db.session.add(nutrition_entry)
    
    # Save all changes
    db.session.commit()
    
    return jsonify({"status": "success", "message": "Data synced successfully"})

def validate_weight_data(record):
    required_fields = ['timestamp', 'weight']
    for field in required_fields:
        if field not in record:
            return False
    try:
        datetime.fromisoformat(record['timestamp'])
        float(record['weight'])
    except ValueError:
        return False
    return True

def validate_body_fat_data(record):
    required_fields = ['timestamp', 'percentage']
    for field in required_fields:
        if field not in record:
            return False
    try:
        datetime.fromisoformat(record['timestamp'])
        float(record['percentage'])
    except ValueError:
        return False
    return True

def validate_calories_data(record):
    required_fields = ['timestamp', 'total_calories']
    for field in required_fields:
        if field not in record:
            return False
    try:
        datetime.fromisoformat(record['timestamp'])
        float(record['total_calories'])
    except ValueError:
        return False
    return True

def validate_nutrition_data(record):
    required_fields = ['timestamp']
    for field in required_fields:
        if field not in record:
            return False
    try:
        datetime.fromisoformat(record['timestamp'])
        if 'calories' in record:
            float(record['calories'])
        if 'protein_grams' in record:
            float(record['protein_grams'])
        if 'carbs_grams' in record:
            float(record['carbs_grams'])
        if 'fat_grams' in record:
            float(record['fat_grams'])
    except ValueError:
        return False
    return True

@health_data_bp.route('/weight', methods=['GET'])
def get_weight_data():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    
    query = WeightRecord.query.filter_by(user_id='your_user_id')
    
    if start_date:
        query = query.filter(WeightRecord.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(WeightRecord.timestamp <= datetime.fromisoformat(end_date))
    
    records = query.order_by(WeightRecord.timestamp).all()
    
    return jsonify([record.to_dict() for record in records])

@health_data_bp.route('/body-fat', methods=['GET'])
def get_body_fat_data():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    
    query = BodyFatRecord.query.filter_by(user_id='your_user_id')
    
    if start_date:
        query = query.filter(BodyFatRecord.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(BodyFatRecord.timestamp <= datetime.fromisoformat(end_date))
    
    records = query.order_by(BodyFatRecord.timestamp).all()
    
    return jsonify([record.to_dict() for record in records])

@health_data_bp.route('/calories', methods=['GET'])
def get_calories_data():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    
    query = CaloriesRecord.query.filter_by(user_id='your_user_id')
    
    if start_date:
        query = query.filter(CaloriesRecord.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(CaloriesRecord.timestamp <= datetime.fromisoformat(end_date))
    
    records = query.order_by(CaloriesRecord.timestamp).all()
    
    return jsonify([record.to_dict() for record in records])

@health_data_bp.route('/nutrition', methods=['GET'])
def get_nutrition_data():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    meal_type = request.args.get('meal_type')
    
    query = NutritionRecord.query.filter_by(user_id='your_user_id')
    
    if start_date:
        query = query.filter(NutritionRecord.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(NutritionRecord.timestamp <= datetime.fromisoformat(end_date))
    if meal_type:
        query = query.filter(NutritionRecord.meal_type == meal_type)
    
    records = query.order_by(NutritionRecord.timestamp).all()
    
    return jsonify([record.to_dict() for record in records])

@health_data_bp.route('/summary/week', methods=['GET'])
def get_weekly_summary():
    """Get a summary of health data for the past week"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    # Get weekly weight average
    weights = WeightRecord.query.filter(
        WeightRecord.user_id == 'your_user_id',
        WeightRecord.timestamp >= start_date,
        WeightRecord.timestamp <= end_date
    ).all()
    
    avg_weight = sum(w.weight_kg for w in weights) / len(weights) if weights else None
    
    # Get latest body fat
    latest_body_fat = BodyFatRecord.query.filter(
        BodyFatRecord.user_id == 'your_user_id',
        BodyFatRecord.timestamp >= start_date
    ).order_by(BodyFatRecord.timestamp.desc()).first()
    
    # Get daily calories
    calories_by_day = {}
    calories = CaloriesRecord.query.filter(
        CaloriesRecord.user_id == 'your_user_id',
        CaloriesRecord.timestamp >= start_date,
        CaloriesRecord.timestamp <= end_date
    ).all()
    
    for record in calories:
        day = record.timestamp.date().isoformat()
        if day not in calories_by_day:
            calories_by_day[day] = 0
        calories_by_day[day] += record.total_calories
    
    return jsonify({
        'avg_weight': avg_weight,
        'latest_body_fat': latest_body_fat.percentage if latest_body_fat else None,
        'calories_by_day': calories_by_day
    })

from flask import Blueprint, request, jsonify
from models import db
from models.weight import WeightRecord
from models.body_fat import BodyFatRecord
from models.calories import CaloriesRecord
from models.nutrition import NutritionRecord
from datetime import datetime, timedelta
import json

health_data_bp = Blueprint('health_data', __name__)

# Existing sync endpoint...

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
        WeightRecord.timestamp >= start_date,
        WeightRecord.timestamp <= end_date
    ).all()
    
    avg_weight = sum(w.weight_kg for w in weights) / len(weights) if weights else None
    
    # Get latest body fat
    latest_body_fat = BodyFatRecord.query.filter(
        BodyFatRecord.timestamp >= start_date
    ).order_by(BodyFatRecord.timestamp.desc()).first()
    
    # Get daily calories
    calories_by_day = {}
    calories = CaloriesRecord.query.filter(
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
import pytest
from backend.app.models.weight import WeightRecord
from backend.app.models.body_fat import BodyFatRecord
from backend.app.models.calories import CaloriesRecord
from backend.app.models.nutrition import NutritionRecord
from datetime import datetime

def test_weight_record():
    record = WeightRecord(
        user_id='test_user',
        timestamp=datetime.utcnow(),
        weight_kg=70.5,
        source='test_source'
    )
    assert record.user_id == 'test_user'
    assert record.weight_kg == 70.5
    assert record.source == 'test_source'
    assert isinstance(record.timestamp, datetime)

def test_body_fat_record():
    record = BodyFatRecord(
        user_id='test_user',
        timestamp=datetime.utcnow(),
        percentage=15.5,
        source='test_source'
    )
    assert record.user_id == 'test_user'
    assert record.percentage == 15.5
    assert record.source == 'test_source'
    assert isinstance(record.timestamp, datetime)

def test_calories_record():
    record = CaloriesRecord(
        user_id='test_user',
        timestamp=datetime.utcnow(),
        active_calories=500,
        basal_calories=1500,
        total_calories=2000,
        source='test_source'
    )
    assert record.user_id == 'test_user'
    assert record.active_calories == 500
    assert record.basal_calories == 1500
    assert record.total_calories == 2000
    assert record.source == 'test_source'
    assert isinstance(record.timestamp, datetime)

def test_nutrition_record():
    record = NutritionRecord(
        user_id='test_user',
        timestamp=datetime.utcnow(),
        calories=2500,
        protein_grams=150,
        carbs_grams=300,
        fat_grams=70,
        meal_type='lunch',
        source='test_source'
    )
    assert record.user_id == 'test_user'
    assert record.calories == 2500
    assert record.protein_grams == 150
    assert record.carbs_grams == 300
    assert record.fat_grams == 70
    assert record.meal_type == 'lunch'
    assert record.source == 'test_source'
    assert isinstance(record.timestamp, datetime)

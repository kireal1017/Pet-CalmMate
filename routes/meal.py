from flask import Blueprint, request, jsonify
from models import Meal
from db import db
from datetime import datetime, timedelta

meal_bp = Blueprint('meal', __name__)

# 식사/간식 기록 추가
@meal_bp.route('/meal', methods=['POST'])
def add_meal():
    data = request.get_json()
    required_fields = ['dog_id', 'meal_datetime', 'meal_amount']
    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    try:
        meal = Meal(
            dog_id=data['dog_id'],
            meal_datetime=datetime.fromisoformat(data['meal_datetime']),
            meal_amount=int(data['meal_amount']),
            memo=data.get('memo')
        )
        db.session.add(meal)
        db.session.commit()

        return jsonify({'message': 'Meal recorded', 'meal_id': meal.meal_id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# 특정 날짜 식사/간식 기록 조회
@meal_bp.route('/meal/list', methods=['GET'])
def get_meal_list():
    dog_id = request.args.get('dog_id', type=int)
    date_str = request.args.get('date')  # "YYYY-MM-DD"

    if not dog_id or not date_str:
        return jsonify({'error': 'dog_id and date are required'}), 400

    try:
        day_start = datetime.fromisoformat(date_str)
        day_end = day_start + timedelta(days=1)

        records = Meal.query.filter(
            Meal.dog_id == dog_id,
            Meal.meal_datetime >= day_start,
            Meal.meal_datetime < day_end
        ).order_by(Meal.meal_datetime).all()

        result = [{
            'meal_id': m.meal_id,
            'meal_datetime': m.meal_datetime.isoformat(),
            'meal_amount': m.meal_amount,
            'memo': m.memo
        } for m in records]

        return jsonify({'dog_id': dog_id, 'date': date_str, 'records': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 식사/간식 기록 수정
@meal_bp.route('/meal', methods=['PUT'])
def update_meal():
    data = request.get_json()
    required_fields = ['meal_id', 'new_meal_amount']
    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    try:
        record = Meal.query.filter_by(meal_id=data['meal_id']).first()
        if not record:
            return jsonify({'error': 'Meal record not found'}), 404

        record.meal_amount = int(data['new_meal_amount'])
        if 'new_memo' in data:
            record.memo = data['new_memo']

        db.session.commit()
        return jsonify({'message': 'Meal updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# 식사/간식 기록 삭제
@meal_bp.route('/meal/<int:meal_id>', methods=['DELETE'])
def delete_meal(meal_id):
    try:
        record = Meal.query.filter_by(meal_id=meal_id).first()
        if not record:
            return jsonify({'error': 'Meal record not found'}), 404

        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': 'Meal record deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

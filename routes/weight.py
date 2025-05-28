# weight.py
''' WeightRecord <- 우리 DB ERD에 없는 테이블
from flask import Blueprint, request, jsonify
from datetime import date
from db import db
from models import WeightRecord  # 모델: id, dog_id, weight, record_date

weight_bp = Blueprint('weight', __name__, url_prefix='/weight')

@weight_bp.route('/add', methods=['POST'])
def add_weight():
    data   = request.get_json()
    dog_id = data.get('dog_id')
    w      = data.get('weight')
    if not dog_id or w is None:
        return jsonify({'error': 'dog_id와 weight를 모두 전달해야 합니다.'}), 400
'''

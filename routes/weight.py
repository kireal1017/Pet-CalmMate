# weight.py
from flask import Blueprint, request, jsonify
from datetime import date
from db import db
from models import WeightRecord

weight_bp = Blueprint('weight', __name__)

# 몸무게 기록 API
@weight_bp.route('/weight', methods=['POST'])
def add_weight():
    data = request.get_json()  # JSON 형식으로 요청 받기

    # 필수값 확인
    required_fields = ['dog_id', 'weight', 'date']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'error': f"Missing fields: {', '.join(missing_fields)}"}), 400

    try:
        # 날짜 변환 및 값 파싱
        record_date = date.fromisoformat(data['date'])  # "YYYY-MM-DD"
        weight = float(data['weight'])

        # 중복 체크: 하루에 한 번만 기록
        existing_record = WeightRecord.query.filter_by(dog_id=data['dog_id'], date=record_date).first()
        if existing_record:
            return jsonify({'error': 'Weight already recorded for this date'}), 409

        # WeightRecord 생성 및 저장
        new_record = WeightRecord(
            dog_id=data['dog_id'],
            weight=weight,
            date=record_date
        )

        db.session.add(new_record)
        db.session.commit()

        return jsonify({
            'message': 'Weight recorded successfully',
            'weight_id': new_record.weight_id
        }), 201

    except ValueError:
        return jsonify({'error': 'Invalid date format or weight value'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    
# 몸무게 수정 api
@weight_bp.route('/weight', methods=['PUT'])
def update_weight():
    data = request.get_json()

    required_fields = ['dog_id', 'date', 'new_weight'] #어떤 강아지의, 어떤 날짜를, 새로운 몸무게
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'error': f"Missing fields: {', '.join(missing_fields)}"}), 400

    try:
        record_date = date.fromisoformat(data['date'])
        new_weight = float(data['new_weight'])

        # 기존 기록 찾기
        record = WeightRecord.query.filter_by(dog_id=data['dog_id'], date=record_date).first()

        if not record:
            return jsonify({'error': 'No existing weight record found for this date'}), 404

        # 몸무게 수정
        record.weight = new_weight
        db.session.commit()

        return jsonify({'message': 'Weight updated successfully'}), 200

    except ValueError:
        return jsonify({'error': 'Invalid date format or weight value'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 몸무게 삭제 API
@weight_bp.route('/weight', methods=['DELETE'])
def delete_weight():
    data = request.get_json()

    required_fields = ['dog_id', 'date']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'error': f"Missing fields: {', '.join(missing_fields)}"}), 400

    try:
        record_date = date.fromisoformat(data['date'])
        record = WeightRecord.query.filter_by(dog_id=data['dog_id'], date=record_date).first()

        if not record:
            return jsonify({'error': 'Weight record not found'}), 404

        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': 'Weight record deleted successfully'}), 200

    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
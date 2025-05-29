from flask import Blueprint, request, jsonify
from datetime import datetime
from db import db
from models import WalkRecord 

walk_bp = Blueprint('walk', __name__) 

# 산책 기록 API
@walk_bp.route('/walk', methods=['POST'])
def add_walk():
    data = request.get_json()  # JSON 요청 받기

    # 필수값 확인
    required_fields = ['dog_id', 'walk_distance', 'walk_duration', 'date_time']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'error': f"Missing fields: {', '.join(missing_fields)}"}), 400

    try:
        walk_distance = float(data['walk_distance'])     # 거리 (ex. 1.2km)
        walk_duration = int(data['walk_duration'])       # 시간 (초 단위)
        record_datetime = datetime.fromisoformat(data['date_time'])  # "YYYY-MM-DDTHH:MM:SS"

        new_record = WalkRecord(
            dog_id=data['dog_id'],
            walk_distance=walk_distance,
            walk_duration=walk_duration,
            date_time=record_datetime
        )

        db.session.add(new_record)
        db.session.commit()

        return jsonify({
            'message': 'Walk recorded successfully',
            'walk_id': new_record.walk_id
        }), 201

    except ValueError:
        return jsonify({'error': 'Invalid data format (datetime, float, or int)'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

#산책 기록 수정 API (사용자가 산책기록을 직접 수정하고 싶을 때 사용. 단, walk_id를 알아야함. 알기위해선 아래 참고)
@walk_bp.route('/walk', methods=['PUT'])
def update_walk():
    data = request.get_json()

    required_fields = ['walk_id', 'new_walk_distance', 'new_walk_duration']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'error': f"Missing fields: {', '.join(missing_fields)}"}), 400

    try:
        walk_id = int(data['walk_id'])
        new_distance = float(data['new_walk_distance'])
        new_duration = int(data['new_walk_duration'])

        # 기존 산책 기록 찾기
        record = WalkRecord.query.filter_by(walk_id=walk_id).first()

        if not record:
            return jsonify({'error': 'No walk record found for given walk_id'}), 404

        # 값 수정
        record.walk_distance = new_distance
        record.walk_duration = new_duration
        db.session.commit()

        return jsonify({'message': 'Walk record updated successfully'}), 200

    except ValueError:
        return jsonify({'error': 'Invalid numeric format'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

#해당 날짜의 산책 기록들을 나타내주는 API. (위 산책기록수정api에서 walk_id를 알기위함)
@walk_bp.route('/walk/list', methods=['GET'])
def get_walk_records_by_date():
    dog_id = request.args.get('dog_id', type=int)
    date_str = request.args.get('date')

    if not dog_id or not date_str:
        return jsonify({'error': 'dog_id and date are required'}), 400

    try:
        from datetime import datetime, timedelta

        # 날짜 파싱
        day_start = datetime.fromisoformat(date_str)
        day_end = day_start + timedelta(days=1)

        # 해당 날짜 범위 내의 기록 필터링
        records = WalkRecord.query.filter(
            WalkRecord.dog_id == dog_id,
            WalkRecord.date_time >= day_start,
            WalkRecord.date_time < day_end
        ).order_by(WalkRecord.date_time).all()

        result = []
        for r in records:
            result.append({
                'walk_id': r.walk_id,
                'date_time': r.date_time.isoformat(),
                'walk_distance': float(r.walk_distance),
                'walk_duration': r.walk_duration  # 초 단위
            })

        return jsonify({
            'dog_id': dog_id,
            'date': date_str,
            'records': result
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

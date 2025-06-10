# routes/device.py
from flask import Blueprint, jsonify, request
import json
from datetime import datetime, timedelta
from models import Meal, Device
from db import db
from .mqtt_iotcore import send_mqtt_message

device_bp = Blueprint('device', __name__)

# 음악 상태 저장: dog_id별로 분리
music_state = {}

@device_bp.route('/dispense-snack', methods=['POST']) #간식주기 API
def dispense_snack():
    data = request.get_json()
    dog_id = data.get('dog_id')
    if not dog_id:
        return jsonify({'error': 'dog_id is required'}), 400

    try:
        # MQTT 메시지 전송
        message = json.dumps({"message": "snack"})
        send_mqtt_message("cmd/control", message)

        # 오늘 날짜의 시작과 끝 구하기
        now = datetime.now() + timedelta(hours=9)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        # 오늘 날짜의 기존 간식 기록 찾기 (food_name 없는 것)
        existing_snack = Meal.query.filter(
            Meal.dog_id == dog_id,
            Meal.meal_datetime >= today_start,
            Meal.meal_datetime < today_end,
            Meal.memo == "자동 간식"
        ).first()

        if existing_snack:
            # 이미 있다면 meal_amount +1
            existing_snack.meal_amount = str(int(existing_snack.meal_amount) + 1)
            existing_snack.meal_datetime = now  # 마지막 시간 업데이트
        else:
            # 없으면 새로 생성
            new_snack = Meal(
                dog_id=dog_id,
                meal_datetime=now,
                meal_amount=1,
                memo="자동 간식"
            )
            db.session.add(new_snack)

        db.session.commit()
        return jsonify({'message': f'간식 배출에 성공했습니다. {dog_id}'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

#음악 재생 요청 -> IoT
@device_bp.route('/music-play', methods=['POST'])
def music_play():
    data = request.get_json()
    dog_id = str(data.get('dog_id'))
    music_type = str(data.get('type'))  # 반드시 문자열로 전송 (0~5)

    if not dog_id:
        return jsonify({'error': 'dog_id is required'}), 400

    if music_type not in ['1', '2', '3', '4', '5']:
        return jsonify({'error': 'type must be 0~5'}), 400

    # MQTT 메시지 전송
    message = json.dumps({
        "message": "music",
        "type": music_type
    })
    send_mqtt_message("cmd/control", message)

    # 상태 저장
    is_playing = False if music_type == '0' else True
    music_state[dog_id] = {
        "is_playing": is_playing,
        "type": music_type
    }

    action = "stopped" if music_type == '0' else f"music #{music_type} played"
    return jsonify({'message': f'{action} for dog {dog_id}'}), 200

# 음악 정지 -> IoT
@device_bp.route('/music-finished', methods=['POST'])
def music_finished():
    data = request.get_json()
    dog_id = str(data.get("dog_id"))

    if not dog_id:
        return jsonify({"error": "dog_id is required"}), 400

    # 상태 갱신
    music_state[dog_id] = {
        "is_playing": False,
        "type": "0"
    }
    message = json.dumps({
        "message": "music",
        "type": "0"
    })
    send_mqtt_message("cmd/control", message)
    return jsonify({"message": f"music finished for dog {dog_id}"}), 200

# 음악 상태 확인(정지인지 재생 중인지) Front에서 확인
@device_bp.route('/music-status', methods=['GET'])
def get_music_status():
    dog_id = request.args.get("dog_id")

    if not dog_id:
        return jsonify({"error": "dog_id is required"}), 400

    state = music_state.get(dog_id, {"is_playing": False, "type": "0"})
    return jsonify(state), 200

#기기 등록 dog_id <-> device_id 매핑
@device_bp.route('/register-device', methods=['POST'])
def register_device():
    data = request.json
    device_id = data.get("device_id")
    dog_id = data.get("dog_id")

    if not device_id or not dog_id:
        return jsonify({"error": "device_id와 dog_id는 필수입니다"}), 400

    # 1. device_id로 기존 기기 찾기
    existing_device = Device.query.filter_by(device_id=device_id).first()

    if existing_device:
        # 2. 이미 등록된 device_id가 있다면, dog_id만 업데이트
        #    이 경우 owner_id와 push_token은 기존 값을 유지하거나 다른 로직으로 처리
        existing_device.dog_id = dog_id
        # existing_device.owner_id = None # 만약 강아지 매핑 시 owner_id를 비워야 한다면 추가 (주의: nullable=False일 경우 오류)
        db.session.commit()
        return jsonify({"message": f"기기 '{device_id}'의 dog_id를 {dog_id}로 업데이트했습니다."}), 200
    else:
        # 3. 새로운 device_id라면, 새로 생성
        #    owner_id와 push_token은 현재 요청에서 받지 않으므로 기본값(None)으로 초기화
        #    만약 Device 모델에 serial_number 등 다른 필수 필드(nullable=False)가 있다면
        #    여기서 해당 값들도 제공해야 합니다.
        new_device = Device(device_id=device_id, dog_id=dog_id, owner_id=None, push_token=None) # owner_id와 push_token을 None으로 명시적 초기화
        db.session.add(new_device)
        db.session.commit()
        return jsonify({"message": "새 기기가 성공적으로 등록되었습니다."}), 201 # 새로 생성했으므로 201 Created 반환


# 당일 간식 준 횟수
@device_bp.route('/snack-today', methods=['GET'])
def get_today_snack_count():
    dog_id = request.args.get('dog_id', type=int)
    if not dog_id:
        return jsonify({'error': 'dog_id is required'}), 400

    try:
        # 오늘 날짜 범위
        now = datetime.now() + timedelta(hours=9)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        # 해당 강아지의 오늘 간식 중 "자동 간식" 기록만 필터
        records = Meal.query.filter(
            Meal.dog_id == dog_id,
            Meal.meal_datetime >= today_start,
            Meal.meal_datetime < today_end
        ).all()

        # meal_amount 합산
        total_snack_amount = sum(int(record.meal_amount) for record in records)

        return jsonify({
            'dog_id': dog_id,
            'date': now.strftime('%Y-%m-%d'),
            'snack_count': total_snack_amount
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
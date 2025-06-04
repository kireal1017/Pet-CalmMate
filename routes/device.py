# routes/device.py
from flask import Blueprint, jsonify, request
import json
from datetime import datetime, timedelta
from models import Meal
from db import db
from .mqtt_iotcore import send_mqtt_message

device_bp = Blueprint('device', __name__)

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
        now = datetime.now()
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
            existing_snack.meal_amount += 1
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
        return jsonify({'message': f'Snack dispensed and recorded for dog {dog_id}'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@device_bp.route('/music-play', methods=['POST']) #노래 재생 API (테스트필요)
def music_play():
    data = request.get_json()
    dog_id = data.get('dog_id')
    if not dog_id:
        return jsonify({'error': 'dog_id is required'}), 400

    message = json.dumps({"message": "music"})
    send_mqtt_message("cmd/control", message)

    return jsonify({'message': f'music command sent to dog {dog_id}.'}), 200

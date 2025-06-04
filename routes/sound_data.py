# sound_data.py
from flask import Blueprint, request, jsonify
from models import db, SoundAnalysis, Device
from collections import defaultdict
from datetime import datetime, timedelta

# device_id 또는 dog_id 기준으로 저장
sound_history = defaultdict(list)

# Blueprint 생성
sound_data_bp = Blueprint('sound', __name__)

# 데이터 저장용 변수
latest_sound_data = {}

#dog_id<->device_id
def get_dog_id_from_device(device_id):
    device = Device.query.filter_by(device_id=device_id).first()
    return device.dog_id if device else None

#불안도레벨 자동부여여
def calculate_anxiety_level(sound_type, confidence, dog_id, timestamp):
    # 기본 점수 테이블
    base_score_map = {
        "Sad": 3,
        "Lonely": 2,
        "Angry": 4,
        "Anxious": 5
    }
    base_score = base_score_map.get(sound_type, 0)

    # confidence 가중치
    if confidence >= 0.9:
        weight = 2.0
    elif confidence >= 0.7:
        weight = 1.5
    elif confidence >= 0.5:
        weight = 1.0
    else:
        weight = 0.5

    # 최근 5분간 짖은 횟수 기록 반영
    now = timestamp
    window_start = now - timedelta(minutes=5)

    # 해당 dog_id의 기록 불러오기
    recent_times = sound_history[dog_id]

    # 현재 timestamp 추가
    recent_times.append(now)

    # 5분 이내로 필터링
    sound_history[dog_id] = [t for t in recent_times if t >= window_start]
    recent_count = len(sound_history[dog_id])

    # 짖은 횟수 보정치 계산
    if recent_count >= 10:
        activity_bonus = 3
    elif recent_count >= 5:
        activity_bonus = 2
    elif recent_count >= 2:
        activity_bonus = 1
    else:
        activity_bonus = 0

    # 최종 anxiety level 계산 (1~10 범위 제한)
    raw_score = base_score * weight + activity_bonus
    anxiety_level = int(min(raw_score, 10))
    return anxiety_level

# 🔹 DB에 데이터 저장하는 함수
def save_to_db(dog_id, anxiety_level, sound_features, record_date):
    new_entry = SoundAnalysis(
        dog_id=dog_id,
        anxiety_level=anxiety_level,
        record_date=record_date,
        sound_features=sound_features
    )
    db.session.add(new_entry)
    db.session.commit()

# POST 요청을 받는 엔드포인트 생성
@sound_data_bp.route('/dog-sound', methods=['POST'])
def receive_sound_data():
    global latest_sound_data
    data = request.json
    print("📌 Received Data:", data)

    if data:
        device_id = data.get("device_id")
        sound_type = data.get("sound_type")
        confidence = data.get("confidence")
        timestamp = data.get("timestamp")

        dog_id = get_dog_id_from_device(device_id)
        if not dog_id:
            return jsonify({"error": "등록되지 않은 device_id입니다"}), 400

        # 예: 불안도 계산
        timestamp_str = data.get("timestamp")
        timestamp_obj = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

        anxiety_level = calculate_anxiety_level(
            sound_type=sound_type,
            confidence=confidence,
            dog_id=dog_id,
            timestamp=timestamp_obj )
        # DB 저장
        save_to_db(
            dog_id=dog_id,
            anxiety_level=anxiety_level,
            sound_features=sound_type,
            record_date=timestamp_obj
        )

        latest_sound_data = {
            **data,
            "anxiety_level": anxiety_level
        }

        return jsonify({"message": "Data received and saved"}), 200
    else:
        return jsonify({"message": "No data received"}), 400

# 프론트엔드로 전달할 엔드포인트 생성
@sound_data_bp.route('/dog-sound', methods=['GET'])
def get_sound_data():
    if latest_sound_data:
        return jsonify(latest_sound_data), 200
    else:
        return jsonify({"message": "No sound data available"}), 404

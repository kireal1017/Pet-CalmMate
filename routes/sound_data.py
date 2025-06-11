# routes/sound_data.py

import json
import time
from threading import Lock
from collections import defaultdict
from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify, Response, current_app
from models import db, SoundAnalysis, Device

# Blueprint 생성
sound_data_bp = Blueprint('sound_data', __name__)

# 데이터 저장용 변수 (GET /dog-sound 용)
latest_sound_data = {}

# 짖음 이력을 남겨두는 저장소 (dog_id별 타임스탬프 리스트)
sound_history = defaultdict(list)

# 알림 이벤트 큐 (SSE용)
notification_queue = []
queue_lock = Lock()


# dog_id 얻어오기 (device_id → dog_id)
def get_dog_id_from_device(device_id):
    device = Device.query.filter_by(device_id=device_id).first()
    return device.dog_id if device else None


# 불안도 레벨 계산 함수
def calculate_anxiety_level(sound_type, confidence, dog_id, timestamp):
    # 기본 점수 맵
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

    # 최근 5분간 짖은 횟수 이력 조회
    now = timestamp
    window_start = now - timedelta(minutes=5)
    recent_times = sound_history[dog_id]

    # 현재 시간 추가
    recent_times.append(now)

    # 5분 이내 타임스탬프만 남겨두기
    sound_history[dog_id] = [t for t in recent_times if t >= window_start]
    recent_count = len(sound_history[dog_id])

    # 활동 보정치 (activity bonus)
    if recent_count >= 10:
        activity_bonus = 3
    elif recent_count >= 5:
        activity_bonus = 2
    elif recent_count >= 2:
        activity_bonus = 1
    else:
        activity_bonus = 0

    # 최종 anxiety level 계산 (최대 10으로 제한)
    raw_score = base_score * weight + activity_bonus
    anxiety_level = int(min(raw_score, 10))
    return anxiety_level


# DB에 데이터 저장
def save_to_db(dog_id, anxiety_level, sound_features, record_datetime):
    new_entry = SoundAnalysis(
        dog_id=dog_id,
        anxiety_level=anxiety_level,
        record_date=record_datetime,
        sound_features=sound_features
    )
    db.session.add(new_entry)
    db.session.commit()


# 알림 큐에 짖음 이벤트 추가
def enqueue_bark_alert(dog_id, timestamp):
    alert = {
        "dog_id": dog_id,
        "alert_time": timestamp.isoformat(),
        "message": "강아지가 짖음이 감지되었습니다!"
    }
    with queue_lock:
        notification_queue.append(alert)


# ─────────────────────────────────────────────────────────────────────────────
# POST /api/dog-sound : 새로운 사운드 데이터 수신
@sound_data_bp.route('/dog-sound', methods=['POST'])
def receive_sound_data():
    global latest_sound_data

    data = request.get_json()
    current_app.logger.info(f"Received Data: {data}")

    if not data:
        return jsonify({"message": "No data received"}), 400

    # 필수 필드 가져오기
    device_id = data.get("device_id")
    sound_type = data.get("sound_type")
    confidence = data.get("confidence")
    timestamp_str = data.get("timestamp")

    if not (device_id and sound_type and confidence is not None and timestamp_str):
        return jsonify({"error": "device_id, sound_type, confidence, timestamp 모두 필요"}), 400

    # device_id → dog_id 매핑
    dog_id = get_dog_id_from_device(device_id)
    if not dog_id:
        return jsonify({"error": "등록되지 않은 device_id입니다"}), 400

    # timestamp 문자열을 datetime 객체로 변환
    try:
        record_datetime_obj = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S") + timedelta(hours=9)
    except ValueError:
        return jsonify({"error": "timestamp 형식은 'YYYY-MM-DD HH:MM:SS' 이어야 합니다."}), 400

    # anxiety level 계산
    try:
        confidence_val = float(confidence)
    except (ValueError, TypeError):
        return jsonify({"error": "confidence는 숫자여야 합니다."}), 400

    anxiety_level = calculate_anxiety_level(
        sound_type=sound_type,
        confidence=confidence_val,
        dog_id=dog_id,
        timestamp=record_datetime_obj
    )

    # DB에 저장
    save_to_db(
        dog_id=dog_id,
        anxiety_level=anxiety_level,
        sound_features=sound_type,
        record_datetime=record_datetime_obj
    )

    # latest_sound_data 갱신 (클라이언트 GET용)
    latest_sound_data = {
        "device_id": device_id,
        "dog_id": dog_id,
        "sound_type": sound_type,
        "confidence": confidence_val,
        "anxiety_level": anxiety_level,
        "timestamp": timestamp_str
    }

    # 짖음 이벤트로 간주하여 알림 큐에 추가
    enqueue_bark_alert(dog_id, datetime.utcnow() + timedelta(hours=9))

    return jsonify({"message": "Data received and saved"}), 200


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/dog-sound : 가장 최근 사운드 데이터 조회
@sound_data_bp.route('/dog-sound', methods=['GET'])
def get_sound_data():
    device_id = request.args.get("device_id")

    if not device_id:
        return jsonify({"error": "device_id가 필요합니다."}), 400

    # Device 테이블에서 device_id 조회
    device = Device.query.filter_by(device_id=device_id).first()
    if not device or not device.dog_id:
        return jsonify({"error": "유효하지 않거나 매핑되지 않은 device_id입니다."}), 404

    dog_id = device.dog_id
    data = latest_sound_data.get(dog_id)

    if data:
        return jsonify(data), 200
    else:
        return jsonify({"message": "해당 device_id에 대한 사운드 데이터가 없습니다."}), 404


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/alert-stream : 알림 스트림 (SSE)
@sound_data_bp.route('/alert-stream')
def alert_stream():
    """
    클라이언트(EventSource)가 연결하여 notification_queue에 쌓인 알림을 실시간 수신.
    """
    def event_generator():
        while True:
            with queue_lock:
                if notification_queue:
                    alert = notification_queue.pop(0)
                else:
                    alert = None

            if alert:
                # SSE 형식: data: {json}\n\n
                yield f"data: {json.dumps(alert, ensure_ascii=False)}\n\n"
            else:
                time.sleep(1)

    return Response(event_generator(), mimetype="text/event-stream")

# GET 불안도
@sound_data_bp.route('/anxiety/list', methods=['GET']) # 또는 anxiety_bp.route
def get_anxiety_records_by_date():
    dog_id = request.args.get('dog_id', type=int)
    date_str = request.args.get('date') # "YYYY-MM-DD" 형식

    # 필수 파라미터 확인
    if not dog_id or not date_str:
        return jsonify({'error': 'dog_id와 date는 필수입니다'}), 400

    try:
        # 날짜 파싱
        # 주어진 날짜의 시작 시간 (00:00:00)
        day_start = datetime.fromisoformat(date_str) + timedelta(hours=9)
        # 주어진 날짜의 다음 날 시작 시간 (24:00:00)
        day_end = day_start + timedelta(days=1)

        # 해당 날짜 범위 내의 SoundAnalysis 기록 필터링
        # record_date 컬럼을 사용합니다 (이전 오류 해결에 기반함)
        records = SoundAnalysis.query.filter(
            SoundAnalysis.dog_id == dog_id,
            SoundAnalysis.record_date >= day_start,
            SoundAnalysis.record_date < day_end
        ).order_by(SoundAnalysis.record_date).all() # 시간 순서대로 정렬

        result = []
        for record in records:
            result.append({
                'analysis_id': record.analysis_id,
                'record_date': record.record_date.isoformat(), # ISO 8601 형식으로 변환
                'sound_type': record.sound_features, # sound_features는 sound_type을 저장한다고 가정
                'anxiety_level': record.anxiety_level
            })

        return jsonify({
            'dog_id': dog_id,
            'date': date_str,
            'records': result
        })

    except ValueError:
        # 날짜 형식 오류 처리
        return jsonify({'error': "잘못된 날짜 형식입니다. 'YYYY-MM-DD' 형식을 사용하세요."}), 400
    except Exception as e:
        # 기타 예외 처리
        return jsonify({'error': str(e)}), 500


# 당일 짖은 횟수
@sound_data_bp.route('/sound-count-today', methods=['GET'])
def get_today_bark_count():
    dog_id = request.args.get('dog_id', type=int)
    if not dog_id:
        return jsonify({'error': 'dog_id is required'}), 400

    try:
        now = datetime.now() + timedelta(hours=9)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        # 오늘 하루 동안의 짖음 기록 수
        count = SoundAnalysis.query.filter(
            SoundAnalysis.dog_id == dog_id,
            SoundAnalysis.record_date >= today_start,
            SoundAnalysis.record_date < today_end
        ).count()

        return jsonify({
            'dog_id': dog_id,
            'date': now.strftime('%Y-%m-%d'),
            'bark_count': count
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
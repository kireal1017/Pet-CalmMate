from flask import Blueprint, request, jsonify
from models import db, Dog, WeightRecord, WalkRecord, SoundAnalysis
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import requests
from config import EC2_PUBLIC_IP

solution_bp = Blueprint('solution_bp', __name__)
AI_BASE_URL = f"http://{EC2_PUBLIC_IP}/gemini"  # 실제 AI 서버 주소로 바꿔야 함

#현재건강상태태
@solution_bp.route('/health-check', methods=['POST'])
def health_check_from_front():
    data = request.get_json()
    dog_id = data.get('dog_id')

    if not dog_id:
        return jsonify({'error': 'dog_id is required'}), 400

    # 1. 강아지 정보 조회
    dog = Dog.query.get(dog_id)
    if not dog:
        return jsonify({'error': 'Dog not found'}), 404

    today = date.today()

    # 2. 체중: 오늘자 없으면 최신 날짜로 대체
    weight_record = (
        WeightRecord.query
        .filter_by(dog_id=dog_id)
        .order_by(WeightRecord.date.desc())
        .first()
    )
    if not weight_record:
        return jsonify({'error': 'No weight record found'}), 400
    weight_kg = float(weight_record.weight)

    # 3. 산책 거리: 오늘자 없으면 최신 날짜로 대체
    walk_record = (
        WalkRecord.query
        .filter_by(dog_id=dog_id)
        .order_by(WalkRecord.date_time.desc())
        .first()
    )
    walk_km = float(walk_record.walk_distance) if walk_record else 0.0

    # 4. 나이 계산 (개월 수)
    age_months = relativedelta(today, dog.birth_date).months + relativedelta(today, dog.birth_date).years * 12

    # 5. AI API에 보낼 데이터 구성
    payload = {
        "breed": dog.breed,
        "age_months": age_months,
        "weight_kg": weight_kg,
        "walk_km": walk_km
    }

    # 6. AI 서버로 POST 요청
    try:
        ai_response = requests.post(f"{AI_BASE_URL}/check_health", json=payload)
        ai_response.raise_for_status()
        return jsonify(ai_response.json()), ai_response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'AI API 요청 실패: {str(e)}'}), 500

#월말 레포트
@solution_bp.route('/monthly-report', methods=['POST'])
def monthly_report_from_front():
    data = request.get_json()
    dog_id = data.get('dog_id')

    if not dog_id:
        return jsonify({'error': 'dog_id is required'}), 400

    # 1. 강아지 정보 조회
    dog = Dog.query.get(dog_id)
    if not dog:
        return jsonify({'error': 'Dog not found'}), 404

    # 2. 오늘 날짜 → 직전 월의 1일 ~ 말일 계산
    today = date.today()
    first_day_of_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day_of_month = date(first_day_of_month.year, first_day_of_month.month, monthrange(first_day_of_month.year, first_day_of_month.month)[1])

    # 3. 체중 변화 리스트 (지난달 1일 ~ 말일)
    weight_records = (
        WeightRecord.query
        .filter(
            WeightRecord.dog_id == dog_id,
            WeightRecord.date >= first_day_of_month,
            WeightRecord.date <= last_day_of_month
        )
        .order_by(WeightRecord.date.asc())
        .all()
    )
    weights = [float(w.weight) for w in weight_records]

    # 4. 산책 거리 변화 리스트
    walk_records = (
        WalkRecord.query
        .filter(
            WalkRecord.dog_id == dog_id,
            WalkRecord.date_time >= datetime.combine(first_day_of_month, datetime.min.time()),
            WalkRecord.date_time <= datetime.combine(last_day_of_month, datetime.max.time())
        )
        .order_by(WalkRecord.date_time.asc())
        .all()
    )
    walk_distances = [float(w.walk_distance) for w in walk_records]

    # 5. 불안도 변화 리스트
    anxiety_records = (
        SoundAnalysis.query
        .filter(
            SoundAnalysis.dog_id == dog_id,
            SoundAnalysis.record_datetime >= datetime.combine(first_day_of_month, datetime.min.time()),
            SoundAnalysis.record_datetime <= datetime.combine(last_day_of_month, datetime.max.time())
        )
        .order_by(SoundAnalysis.record_datetime.asc())
        .all()
    )
    anxiety_scores = [
        round(min(1.0, max(0.0, a.anxiety_level / 10.0)), 2)
        for a in anxiety_records if a.anxiety_level is not None
    ]

    # 6. 나이 계산 (해당 월 말 기준)
    age_months = (
        relativedelta(last_day_of_month, dog.birth_date).months +
        relativedelta(last_day_of_month, dog.birth_date).years * 12
    )

    # 7. AI API에 보낼 데이터 구성
    payload = {
        "breed": dog.breed,
        "age_months": age_months,
        "weights": weights,
        "walk_distances": walk_distances,
        "anxiety_scores": anxiety_scores
    }

    # 8. AI 서버로 POST 요청
    try:
        ai_response = requests.post(f"{AI_BASE_URL}/monthly_report", json=payload)
        ai_response.raise_for_status()
        return jsonify(ai_response.json()), ai_response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'AI API 요청 실패: {str(e)}'}), 500
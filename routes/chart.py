from flask import Blueprint, request, jsonify
from db import db
from models import WeightRecord, WalkRecord, Meal, SoundAnalysis
from sqlalchemy import extract
import calendar
from datetime import datetime, timedelta

chart_bp = Blueprint('chart', __name__)

# 월간 체중 그래프: 일별 체중 (30~31일)
@chart_bp.route('/chart/weight', methods=['GET'])
def get_weight_chart():
    dog_id = request.args.get('dog_id', type=int)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)

    if not dog_id or not year or not month:
        return jsonify({'error': 'dog_id, year, month are required'}), 400

    try:
        days_in_month = calendar.monthrange(year, month)[1]
        weights = [None] * days_in_month

        records = WeightRecord.query.filter(
            WeightRecord.dog_id == dog_id,
            extract('year', WeightRecord.date) == year,
            extract('month', WeightRecord.date) == month
        ).all()

        for record in records:
            day = record.date.day
            weights[day - 1] = float(record.weight)

        return jsonify({
            'dog_id': dog_id,
            'year': year,
            'month': month,
            'weights': weights
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 연간 체중 그래프: 월별 평균 체중 (12개)
@chart_bp.route('/chart/weight/yearly', methods=['GET'])
def get_yearly_weight_chart():
    dog_id = request.args.get('dog_id', type=int)
    year = request.args.get('year', type=int)

    if not dog_id or not year:
        return jsonify({'error': 'dog_id and year are required'}), 400

    try:
        monthly_avg_weights = [None] * 12

        records = WeightRecord.query.filter(
            WeightRecord.dog_id == dog_id,
            extract('year', WeightRecord.date) == year
        ).all()

        weight_data_by_month = {month: [] for month in range(1, 13)}
        for record in records:
            if record.weight is not None:
                weight_data_by_month[record.date.month].append(float(record.weight))

        for month in range(1, 13):
            weights = weight_data_by_month[month]
            if weights:
                monthly_avg_weights[month - 1] = round(sum(weights) / len(weights), 2)

        return jsonify({
            'dog_id': dog_id,
            'year': year,
            'monthly_avg_weights': monthly_avg_weights
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 월간 산책량 API
@chart_bp.route('/chart/walk/distance', methods=['GET'])
def get_walk_distance_chart():
    dog_id = request.args.get('dog_id', type=int)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)

    if not dog_id or not year or not month:
        return jsonify({'error': 'dog_id, year, month are required'}), 400

    try:
        days_in_month = calendar.monthrange(year, month)[1]
        walk_sums = [0.0] * days_in_month

        records = WalkRecord.query.filter(
            WalkRecord.dog_id == dog_id,
            extract('year', WalkRecord.date_time) == year,
            extract('month', WalkRecord.date_time) == month
        ).all()

        for record in records:
            day = record.date_time.day
            walk_sums[day - 1] += float(record.walk_distance)

        walks = [round(w, 2) if w > 0 else None for w in walk_sums]

        return jsonify({
            'dog_id': dog_id,
            'year': year,
            'month': month,
            'walk_distances': walks
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 월간 산책시간 API
@chart_bp.route('/chart/walk/duration', methods=['GET'])
def get_walk_duration_chart():
    dog_id = request.args.get('dog_id', type=int)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)

    if not dog_id or not year or not month:
        return jsonify({'error': 'dog_id, year, month are required'}), 400

    try:
        days_in_month = calendar.monthrange(year, month)[1]
        duration_sums = [0] * days_in_month

        records = WalkRecord.query.filter(
            WalkRecord.dog_id == dog_id,
            extract('year', WalkRecord.date_time) == year,
            extract('month', WalkRecord.date_time) == month
        ).all()

        for record in records:
            day = record.date_time.day
            duration_sums[day - 1] += record.walk_duration

        durations = [d if d > 0 else None for d in duration_sums]

        return jsonify({
            'dog_id': dog_id,
            'year': year,
            'month': month,
            'walk_durations': durations  # 단위: 초
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
# 월간 간식/식사량 합계 차트
@chart_bp.route('/chart/meal', methods=['GET'])
def get_meal_chart():
    dog_id = request.args.get('dog_id', type=int)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)

    if not dog_id or not year or not month:
        return jsonify({'error': 'dog_id, year, month are required'}), 400

    try:
        days_in_month = calendar.monthrange(year, month)[1]
        meal_sums = [0] * days_in_month  # 하루마다 누적합 저장

        records = Meal.query.filter(
            Meal.dog_id == dog_id,
            extract('year', Meal.meal_datetime) == year,
            extract('month', Meal.meal_datetime) == month
        ).all()

        for record in records:
            day = record.meal_datetime.day
            meal_sums[day - 1] += int(record.meal_amount)

        # 0은 None으로 표시 (미기록일 경우)
        meals = [s if s > 0 else None for s in meal_sums]

        return jsonify({
            'dog_id': dog_id,
            'year': year,
            'month': month,
            'meals': meals
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# 일간 식사/간식 시간별 차트 (1시간 단위)
@chart_bp.route('/chart/meal/daily', methods=['GET'])
def get_meal_daily_chart():
    dog_id = request.args.get('dog_id', type=int)
    date_str = request.args.get('date')  # YYYY-MM-DD

    if not dog_id or not date_str:
        return jsonify({'error': 'dog_id and date are required'}), 400

    try:
        start = datetime.fromisoformat(date_str)
        end = start + timedelta(days=1)

        records = Meal.query.filter(
            Meal.dog_id == dog_id,
            Meal.meal_datetime >= start,
            Meal.meal_datetime < end
        ).all()

        hourly_sums = [0] * 24

        for record in records:
            hour = record.meal_datetime.hour
            hourly_sums[hour] += int(record.meal_amount)

        meals = [s if s > 0 else None for s in hourly_sums]

        return jsonify({
            'dog_id': dog_id,
            'date': date_str,
            'meals': meals  # 각 index는 시간 (0~23시)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 월간 불안도 차트
@chart_bp.route('/chart/anxiety', methods=['GET'])
def get_monthly_anxiety_chart():
    dog_id = request.args.get('dog_id', type=int)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)

    if not dog_id or not year or not month:
        return jsonify({'error': 'dog_id, year, month are required'}), 400

    try:
        days_in_month = calendar.monthrange(year, month)[1]
        anxiety_by_day = [[] for _ in range(days_in_month)]

        records = SoundAnalysis.query.filter(
            SoundAnalysis.dog_id == dog_id,
            extract('year', SoundAnalysis.record_date) == year,
            extract('month', SoundAnalysis.record_date) == month
        ).all()

        for record in records:
            if record.anxiety_level is None:
                continue
            day = record.record_date.day
            if 1 <= day <= days_in_month:
                anxiety_by_day[day - 1].append(record.anxiety_level)

        daily_avg_anxieties = []
        for values in anxiety_by_day:
            if values:
                avg = round(sum(values) / len(values), 2)
                daily_avg_anxieties.append(avg)
            else:
                daily_avg_anxieties.append(0)  # ⬅️ 데이터 없으면 0으로 채움
        print(f"[DEBUG] 응답 데이터: {daily_avg_anxieties}")
        return jsonify({
            'dog_id': dog_id,
            'year': year,
            'month': month,
            'daily_avg_anxieties': daily_avg_anxieties
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


# 일간 불안도 차트
@chart_bp.route('/chart/anxiety/daily', methods=['GET'])
def get_daily_anxiety_chart():
    dog_id = request.args.get('dog_id', type=int)
    date_str = request.args.get('date')  # YYYY-MM-DD

    if not dog_id or not date_str:
        return jsonify({'error': 'dog_id and date are required'}), 400

    try:
        from models import SoundAnalysis
        start = datetime.fromisoformat(date_str)
        end = start + timedelta(days=1)

        # 시간별 불안도 목록 초기화 (0시 ~ 23시)
        hourly_anxiety = [[] for _ in range(24)]

        # 해당 날짜의 기록 조회
        records = SoundAnalysis.query.filter(
            SoundAnalysis.dog_id == dog_id,
            SoundAnalysis.record_date >= start,
            SoundAnalysis.record_date < end
        ).all()

        # 각 시간대에 불안도 값 추가
        for record in records:
            if record.anxiety_level is None:
                continue
            hour = record.record_date.hour
            if 0 <= hour <= 23:
                hourly_anxiety[hour].append(record.anxiety_level)

        # 시간별 평균 불안도 계산 (없으면 0)
        hourly_avg_anxieties = [
            round(sum(values)/len(values), 2) if values else 0
            for values in hourly_anxiety
        ]

        return jsonify({
            'dog_id': dog_id,
            'date': date_str,
            'hourly_avg_anxieties': hourly_avg_anxieties
        }), 200

    except ValueError:
        return jsonify({'error': "날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식이어야 합니다."}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
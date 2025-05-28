from flask import Blueprint, request, jsonify
from db import db
from models import CareRecord
from sqlalchemy import extract
import calendar

chart_bp = Blueprint('chart', __name__)

#월 차트 (일별 체중 30개개)
@chart_bp.route('/chart/weight', methods=['GET'])
def get_weight_chart():
    dog_id = request.args.get('dog_id', type=int)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)

    if not dog_id or not year or not month:
        return jsonify({'error': 'dog_id, year, month are required'}), 400

    try:
        # 해당 월의 일 수만큼 빈 리스트 생성
        days_in_month = calendar.monthrange(year, month)[1]
        weights = [None] * days_in_month

        # 해당 월에 해당하는 CareRecord 필터링
        records = CareRecord.query.filter(
            CareRecord.dog_id == dog_id,
            extract('year', CareRecord.date) == year,
            extract('month', CareRecord.date) == month
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

#연도별 차트(월별 체중 12개)
@chart_bp.route('/chart/weight/yearly', methods=['GET'])
def get_yearly_weight_chart():
    dog_id = request.args.get('dog_id', type=int)
    year = request.args.get('year', type=int)

    if not dog_id or not year:
        return jsonify({'error': 'dog_id and year are required'}), 400

    try:
        # 1월부터 12월까지 평균 체중을 담을 리스트
        monthly_avg_weights = [None] * 12

        # 해당 강아지의 연도별 기록을 모두 가져오기
        records = CareRecord.query.filter(
            CareRecord.dog_id == dog_id,
            extract('year', CareRecord.date) == year
        ).all()

        # 월별로 체중 데이터를 그룹핑
        weight_data_by_month = {month: [] for month in range(1, 13)}
        for record in records:
            if record.weight is not None:
                weight_data_by_month[record.date.month].append(float(record.weight))

        # 월별 평균 체중 계산 (리스트에서 30개의 요소를 가져와 평균값을 해당 월에 대입)
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
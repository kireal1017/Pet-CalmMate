'''# routes/walk.py 일단 임시로 냅둠.
from flask import Blueprint, request, jsonify
from db import get_connection
import datetime, logging
import pymysql

walk_bp = Blueprint('walk', __name__)

@walk_bp.route('/walk', methods=['POST'])
def create_walk():
    """
    클라이언트에서 넘어오는 JSON 예시:
    {
      "user_id": "user123",
      "walk_date": "2025-04-20",   # YYYY-MM-DD
      "walk_time": "07:30:00",     # HH:MM:SS
      "duration": "01:10:00",      # HH:MM:SS
      "distance": 8.0              # km (float)
    }
    """
    data = request.get_json() or {}
    user_id   = data.get('user_id')
    date_str  = data.get('walk_date')
    time_str  = data.get('walk_time')
    dur_str   = data.get('duration')
    dist      = data.get('distance')

    # 필수 파라미터 확인
    if not all([user_id, date_str, time_str, dur_str is not None, dist is not None]):
        return jsonify({'success': False, 'error': '필수 파라미터 누락'}), 400

    # 문자열 → Python 객체 변환
    try:
        walk_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        walk_time = datetime.datetime.strptime(time_str, '%H:%M:%S').time()
        duration  = datetime.datetime.strptime(dur_str, '%H:%M:%S').time()
        distance  = float(dist)
    except ValueError as e:
        return jsonify({'success': False, 'error': f'포맷 오류: {e}'}), 400

    # 거리 유효성 검사
    if distance < 0:
        return jsonify({'success': False, 'error': 'distance는 0 이상이어야 합니다.'}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            sql = """
                INSERT INTO walks
                  (user_id, walk_date, walk_time, duration, distance)
                VALUES (%s, %s, %s, %s, %s)
            """
            cur.execute(sql, (user_id, walk_date, walk_time, duration, distance))
        conn.commit()
        walk_id = cur.lastrowid
        logging.info(f"[WALK] user={user_id} walk_id={walk_id}")
        return jsonify({'success': True, 'walk_id': walk_id}), 201

    except pymysql.MySQLError as e:
        logging.error(f"[WALK ERROR] {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

    finally:
        conn.close()
'''
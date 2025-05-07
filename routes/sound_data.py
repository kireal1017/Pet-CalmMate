# sound_data.py
from flask import Blueprint, request, jsonify

# Blueprint 생성
sound_bp = Blueprint('sound', __name__)

# 데이터 저장용 변수
latest_sound_data = {}

# POST 요청을 받는 엔드포인트 생성
@sound_bp.route('/api/dog-sound', methods=['POST'])
def receive_sound_data():
    global latest_sound_data
    data = request.json
    
    # 데이터 저장
    if data:
        latest_sound_data = data
        return jsonify({"message": "Data received successfully"}), 200
    else:
        return jsonify({"message": "No data received"}), 400

# 프론트엔드로 전달할 엔드포인트 생성
@sound_bp.route('/api/dog-sound', methods=['GET'])
def get_sound_data():
    if latest_sound_data:
        return jsonify(latest_sound_data), 200
    else:
        return jsonify({"message": "No sound data available"}), 404

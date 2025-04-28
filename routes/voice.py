# routes/voice.py
from flask import Blueprint, jsonify

voice_bp = Blueprint('voice', __name__)

@voice_bp.route('/play', methods=['POST'])
def play_voice():
    """스피커로 음성 출력"""
    # TODO: 실제 음성 재생 로직
    return jsonify({"result": "ok", "message": "음성 출력 완료!"})

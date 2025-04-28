from flask import Blueprint, jsonify

voice_bp = Blueprint('voice', __name__)

# 🎤 마이크 토글용 (React 버튼용)
@voice_bp.route('/mic/toggle', methods=['POST'])
def toggle_mic():
    return jsonify({"mic_on": True})

# 🔊 음성 출력용 (스피커 음성 출력용)
@voice_bp.route('/play', methods=['POST'])
def play_voice():
    # 실제 음성 출력 로직은 이곳에 구현
    return jsonify({"result": "ok", "message": "음성 출력 완료!"})

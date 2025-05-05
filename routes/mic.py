from flask import Blueprint, jsonify

mic_bp = Blueprint('mic', __name__)

# —————— 전역 상태 ——————
mic_on = False

@mic_bp.route('/mic/toggle', methods=['POST'])
def toggle_mic():
    """마이크 On/Off 토글"""
    global mic_on
    mic_on = not mic_on
    return jsonify({'mic_on': mic_on})

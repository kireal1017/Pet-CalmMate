from flask import Blueprint, jsonify
from .mqtt_iotcore import send_mqtt_message  # MQTT 전송 함수 import

mic_bp = Blueprint('mic', __name__)

# —————— 전역 상태 ——————
mic_on = False

@mic_bp.route('/mic/toggle', methods=['POST'])
def toggle_mic():
    """마이크 On/Off 토글 및 MQTT 전송"""
    global mic_on
    mic_on = not mic_on

    # MQTT 메시지 전송
    topic = "cmd/mic"
    message = "on" if mic_on else "off" #수정 필요 문자열이 아닌 dumps로 보내야함 on/off
    send_mqtt_message(topic, message)

    return jsonify({'mic_on': mic_on})

#근데 마이크도 On/OFF를 하는게 맞음????????????
# routes/device.py
from flask import Blueprint, jsonify
import paho.mqtt.client as mqtt

device_bp = Blueprint('device', __name__)

# MQTT 세팅 (모듈 로딩 시 한 번만)
MQTT_BROKER = "localhost"
MQTT_PORT   = 1883

mqtt_client = mqtt.Client(protocol=mqtt.MQTTv311)
try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
    print(f"[MQTT] Connected to {MQTT_BROKER}:{MQTT_PORT}")
except Exception as e:
    print(f"[MQTT] Connection failed: {e}")

@device_bp.route('/dispense-snack', methods=['POST'])
def dispense_snack():
    """간식 디스펜서에 MQTT 명령 발행"""
    try:
        mqtt_client.publish('pet/dispense', payload='SNACK', qos=1)
        return jsonify({'success': True, 'message': '간식 발행 완료'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

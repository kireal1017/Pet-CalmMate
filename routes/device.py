# routes/device.py
from flask import Blueprint, jsonify, Response, request
import cv2, time
from .mqtt_iotcore import send_mqtt_message

device_bp = Blueprint('device', __name__)

@device_bp.route('/dispense-snack', methods=['POST']) #간식주기 API
def dispense_snack():
    data = request.get_json()
    dog_id = data.get('dog_id')
    if not dog_id:
        return jsonify({'error': 'dog_id is required'}), 400

    topic = f"cmd/control"
    message = "snack"
    send_mqtt_message(topic, message)

    return jsonify({'message': f'Snack dispense command sent to dog {dog_id}.'}), 200

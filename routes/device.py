# routes/device.py
from flask import Blueprint, jsonify, Response, request
import cv2, time
from mqtt_iotcore import send_mqtt_message

device_bp = Blueprint('device', __name__)

camera_on = False
video_capture = cv2.VideoCapture(0)

@device_bp.route('/camera/toggle', methods=['POST'])
def toggle_camera():
    global camera_on
    camera_on = not camera_on
    return jsonify({'camera_on': camera_on})

@device_bp.route('/mic/toggle', methods=['POST'])
def toggle_mic():
    return jsonify({'mic_on': True})

@device_bp.route('/dispense-snack', methods=['POST'])
def dispense_snack():
    data = request.get_json()
    dog_id = data.get('dog_id')
    if not dog_id:
        return jsonify({'error': 'dog_id is required'}), 400

    topic = f"nyangmeong/dog{dog_id}/dispense"
    message = "SNACK"
    send_mqtt_message(topic, message)

    return jsonify({'message': f'Snack dispense command sent to dog {dog_id}.'}), 200

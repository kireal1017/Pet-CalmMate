
from flask import Blueprint, jsonify, request
from routes.mqtt_iotcore import send_mqtt_message

device_bp = Blueprint('device', __name__)

@device_bp.route('/treat', methods=['POST'])
def give_treat():
    data = request.get_json()
    dog_id = data.get('dog_id')
    if not dog_id:
        return jsonify({'error': 'dog_id is required'}), 400

    topic = f"nyangmeong/dog{dog_id}/treat"
    message = "Give treat!"
    send_mqtt_message(topic, message)

    return jsonify({'message': f'Treat command sent to dog {dog_id}.'}), 200
# routes/device.py
from flask import Blueprint, jsonify, Response, request
import cv2, time
import paho.mqtt.client as mqtt

device_bp = Blueprint('device', __name__)

# MQTT 설정
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

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
    mqtt_client.publish("pet/dispense", payload="SNACK", qos=1)
    return jsonify({"success": True, "message": "MQTT 간식 신호 발행 완료"})

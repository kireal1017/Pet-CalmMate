# routes/camera.py
from flask import Blueprint, jsonify, request
from .mqtt_iotcore import send_mqtt_message
import json, os
import logging
from config import RTMP_STREAM_ID, HLS_BASE_URL, EC2_PUBLIC_IP
from datetime import datetime, timedelta


camera_bp = Blueprint('camera', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@camera_bp.route('/camera/stream-url', methods=['GET'])
def get_hls_stream_url():
    """
    HLS 스트림 URL을 반환하는 API (환경변수 기반)
    """
    try:
        hls_url = f"{HLS_BASE_URL}/{RTMP_STREAM_ID}.m3u8"
        return jsonify({'stream_url': hls_url}), 200
    except Exception as e:
        logger.error(f"[HLS URL 생성 실패] {str(e)}")
        return jsonify({'error': str(e)}), 500

# 📡 카메라 ON API (MQTT 전송)
@camera_bp.route('/camera/on', methods=['POST'])
def mqtt_camera_on():
    message = json.dumps({"message": "camera_on"})
    send_mqtt_message("cmd/control", message)
    return jsonify({"status": "camera_on signal sent"})


# 📡 카메라 OFF API (MQTT 전송)
@camera_bp.route('/camera/off', methods=['POST'])
def mqtt_camera_off():
    message = json.dumps({"message": "camera_off"})
    send_mqtt_message("cmd/control", message)
    return jsonify({"status": "camera_off signal sent"})

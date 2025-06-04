# routes/camera.py
from flask import Blueprint, jsonify, request
from .mqtt_iotcore import send_mqtt_message
import boto3, json, os
import logging
from config import RTMP_STREAM_ID, HLS_BASE_URL, EC2_PUBLIC_IP

camera_bp = Blueprint('camera', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@camera_bp.route('/camera/stream-url', methods=['GET'])
def get_kvs_hls_stream_url():
    """
    EC2에서 중계되는 HLS 스트림 URL을 제공하는 API 엔드포인트
    """
    try:
        # 기본 HLS URL 구성
        stream_id = RTMP_STREAM_ID  # ex: "kvs-stream"
        hls_url = f"http://{EC2_PUBLIC_IP}/hls/{stream_id}.m3u8"

        # 기본 응답 반환
        return jsonify({
            'stream_url': hls_url
        }), 200

    except Exception as e:
        logger.exception("Error building HLS stream URL")
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

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
def get_kvs_stream_url():
    try:
        # 여기서 media_client 생성하고, get_hls_streaming_session_url 호출
        media_client = boto3.client("kinesisvideo")
        endpoint = media_client.get_data_endpoint(
            StreamName="YourStreamName",
            APIName="GET_HLS_STREAMING_SESSION_URL"
        )['DataEndpoint']

        media_client = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint)
        hls_url = media_client.get_hls_streaming_session_url(
            StreamName="YourStreamName",
            PlaybackMode='LIVE'
        )['HLSStreamingSessionURL']

        return jsonify({'stream_url': hls_url})
    except Exception as e:
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

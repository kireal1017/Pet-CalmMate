# routes/camera.py
from flask import Blueprint, jsonify, request
from .mqtt_iotcore import send_mqtt_message
import boto3, json, os

camera_bp = Blueprint('camera', __name__)

# HLS 스트림 URL 제공 API (즉, 실시간 스트리밍 URL 제공)
@camera_bp.route('/camera/stream-url', methods=['GET'])
def get_kvs_stream_url():
    stream_name = "rpi-video"
    region = "ap-northeast-2"

    # 1. KVS 엔드포인트 요청
    kvs_client = boto3.client('kinesisvideo', region_name=region)
    endpoint = kvs_client.get_data_endpoint(
        StreamName=stream_name,
        APIName='GET_HLS_STREAMING_SESSION_URL'
    )['DataEndpoint']

    # 2. HLS URL 요청
    media_client = boto3.client('kinesis-video-archived-media',
                                 endpoint_url=endpoint,
                                 region_name=region)
    hls_url = media_client.get_hls_streaming_session_url(
        StreamName=stream_name,
        PlaybackMode='LIVE'
    )['HLSStreamingSessionURL']

    return jsonify({'stream_url': hls_url})


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

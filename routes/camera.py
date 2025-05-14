# routes/camera.py
from flask import Blueprint, jsonify, request
from .mqtt_iotcore import send_mqtt_message
import boto3, json, os

camera_bp = Blueprint('camera', __name__)

# HLS 스트림 URL 제공 API (즉, 실시간 스트리밍 URL 제공)
@camera_bp.route('/camera/stream-url', methods=['GET'])
def get_ivs_stream_url():
    stream_name = "rpi-stream"
    region = "ap-northeast-2"

    # 1. IVS 클라이언트 생성
    ivs_client = boto3.client('ivs', region_name=region)

    # 2. 채널 목록 불러오기 (채널 이름으로 필터링)
    response = ivs_client.list_channels(
        filterByName=channel_name
    )

    # 3. 채널 ARN 가져오기
    if not response['channels']:
        return jsonify({'error': 'Channel not found'}), 404

    channel_arn = response['channels'][0]['arn']

    # 4. IVS 플레이백 URL 생성
    playback_url = f"https://{channel_arn}.ivs.{{region}}.amazonaws.com/hls/v1/{channel_arn}/master.m3u8".format(region=region)

    return jsonify({'stream_url': playback_url})


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

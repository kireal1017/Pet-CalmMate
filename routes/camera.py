# routes/camera.py
from flask import Blueprint, jsonify, request
from .mqtt_iotcore import send_mqtt_message
import boto3, json, os
import logging
from config import IVS_CHANNEL_NAME, IVS_REGION

camera_bp = Blueprint('camera', __name__)

# 🔄 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔄 IVS 클라이언트 생성
ivs_client = boto3.client('ivs', region_name=IVS_REGION)

@camera_bp.route('/stream-url', methods=['GET'])
def get_ivs_stream_url():
    try:
        # 🔄 1. IVS 채널 목록 가져오기
        logger.info(f"Fetching IVS Channel List for Channel: {IVS_CHANNEL_NAME}")
        
        response = ivs_client.list_channels(
            filterByName=IVS_CHANNEL_NAME
        )

        # 🔄 2. 채널이 없을 때 처리
        if not response['channels']:
            logger.error(f"Channel not found: {IVS_CHANNEL_NAME}")
            return jsonify({'error': 'Channel not found'}), 404

        # 🔄 3. 채널 ARN 및 Playback URL 추출
        channel_arn = response['channels'][0]['arn']
        playback_url = response['channels'][0]['playbackUrl']

        logger.info(f"Channel ARN: {channel_arn}")
        logger.info(f"Playback URL: {playback_url}")

        # 🔄 4. 결과 반환
        return jsonify({
            'stream_url': playback_url
        }), 200

    except Exception as e:
        logger.exception("Error fetching IVS stream URL")
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

# audio.py
import os
import logging
from flask import Blueprint, request, jsonify, current_app
import boto3
from werkzeug.utils import secure_filename

# 로깅
logging.basicConfig(level=logging.INFO)

# 블루프린트 설정
audio_bp = Blueprint('audio', __name__, url_prefix='/api/audio')

# 허용 확장자
ALLOWED_EXT = {'wav'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

# AWS IoT Data Plane 클라이언트 초기화
def get_iot_client():
    endpoint = os.getenv('AWS_IOT_ENDPOINT')
    region   = os.getenv('AWS_REGION')
    return boto3.client(
        'iot-data',
        region_name=region,
        endpoint_url=f'https://{endpoint}'
    )

@audio_bp.route('/upload', methods=['POST'])
def upload_audio():
    # 1) 파일 존재 확인
    if 'file' not in request.files:
        return jsonify({'error': '파일이 업로드되지 않았습니다.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '파일명이 비어 있습니다.'}), 400

    # 2) 확장자 검증
    if not allowed_file(file.filename):
        return jsonify({'error': 'wav 파일만 업로드할 수 있습니다.'}), 400

    filename = secure_filename(file.filename)
    # (선택) 서버에 임시 저장
    temp_path = os.path.join('/tmp', filename)
    file.save(temp_path)
    logging.info(f"Received audio file: {temp_path}")

    # 3) MQTT 퍼블리시
    try:
        iot = get_iot_client()
        with open(temp_path, 'rb') as f:
            audio_bytes = f.read()

        # petcare/audio 토픽으로 전송 (QoS 1)
        resp = iot.publish(
            topic='petcare/audio',
            qos=1,
            payload=audio_bytes
        )
        logging.info(f"Published to MQTT topic: petcare/audio")
    except Exception as e:
        logging.error(f"MQTT publish error: {e}")
        return jsonify({'error': 'MQTT 전송 중 오류가 발생했습니다.'}), 500
    finally:
        # (선택) 임시 파일 삭제
        try:
            os.remove(temp_path)
        except OSError:
            pass

    return jsonify({'message': '업로드 및 MQTT 전송 완료'}), 200

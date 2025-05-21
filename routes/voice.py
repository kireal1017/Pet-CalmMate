from flask import Blueprint, request, jsonify
from .mqtt_iotcore import send_mqtt_message
import os, uuid, json, threading, time

voice_bp = Blueprint('voice', __name__)

UPLOAD_FOLDER = './static/voice'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def delayed_delete(filepath, delay=10):
    """지정한 시간 후 파일 삭제"""
    time.sleep(delay)
    try:
        os.remove(filepath)
        print(f"[삭제됨] {filepath}")
    except Exception as e:
        print(f"[삭제 실패] {filepath}: {e}")

@voice_bp.route('/speak-upload', methods=['POST'])
def upload_and_play_voice():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if not file.filename.endswith('.wav'):
        return jsonify({'error': 'Only .wav files allowed'}), 400

    # 고유 파일명 생성 후 저장
    filename = f"{uuid.uuid4().hex}.wav"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # URL 생성
    public_url = f"http://<EC2_PUBLIC_IP>/static/voice/{filename}"

    # MQTT 메시지 전송
    message = {
        "command": "play_audio",
        "url": public_url
    }
    send_mqtt_message("cmd/control", json.dumps(message))

    # 삭제 스케줄 (10초 후)
    threading.Thread(target=delayed_delete, args=(filepath, 10)).start()

    return jsonify({'result': 'ok', 'message': '음성 재생 요청 완료'})
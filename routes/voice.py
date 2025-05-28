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
    print("[🔔] API 호출됨")

    if 'file' not in request.files:
        print("[❌] file 없음")
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    print(f"[📁] 파일 이름: {file.filename}")

    if not file.filename.endswith('.m4a'):
        print("[❌] 확장자 오류")
        return jsonify({'error': 'Only .m4a files allowed'}), 400

    filename = f"{uuid.uuid4().hex}.m4a"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    print(f"[✅] 파일 저장 완료: {filepath}")

    public_url = f"http://54.180.212.150/static/voice/{filename}"
    message = {
        "message": "speaker",
        "url": public_url
    }
    print(f"[📤] MQTT 전송: {json.dumps(message)}")
    send_mqtt_message("cmd/control", json.dumps(message))

    threading.Thread(target=delayed_delete, args=(filepath, 10)).start()
    print("[🚀] 삭제 스레드 실행됨")

    return jsonify({'result': 'ok', 'message': 'voice speak complete'})

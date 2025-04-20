# app.py
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import time
import cv2
import paho.mqtt.client as mqtt

# 기존 블루프린트 import
from routes.user import user_bp
from routes.dog import dog_bp

app = Flask(__name__)
CORS(app)

# —————— 블루프린트 등록 ——————
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(dog_bp, url_prefix='/api')

# —————— 전역 상태 ——————
camera_on = False
mic_on = False

# OpenCV 비디오 캡처 (Raspberry Pi 카메라 또는 USB 카메라)
video_capture = cv2.VideoCapture(0)

# MQTT 설정 (IoT 디바이스 제어용)
MQTT_BROKER = "YOUR_MQTT_BROKER_IP"
MQTT_PORT   = 1883
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# —————— 비디오 스트리밍 제너레이터 ——————
def gen_frames():
    global camera_on
    while True:
        if not camera_on:
            time.sleep(0.1)
            continue

        success, frame = video_capture.read()
        if not success:
            break

        # JPEG 인코딩
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # MJPEG 스트림 형식으로 yield
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# —————— API 라우트 정의 ——————

@app.route('/api/stream')
def stream():
    """카메라가 켜져 있으면 MJPEG 스트림을 내려줌"""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/camera/toggle', methods=['POST'])
def toggle_camera():
    """카메라 On/Off 토글"""
    global camera_on
    camera_on = not camera_on
    return jsonify({'camera_on': camera_on})

@app.route('/api/mic/toggle', methods=['POST'])
def toggle_mic():
    """마이크 On/Off 토글"""
    global mic_on
    mic_on = not mic_on
    return jsonify({'mic_on': mic_on})

@app.route('/api/dispense-snack', methods=['POST'])
def dispense_snack():
    """간식 디스펜서에 MQTT 명령 발행"""
    try:
        mqtt_client.publish('pet/dispense', payload='SNACK', qos=1)
        return jsonify({'success': True, 'message': '간식을 지급했습니다.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # 디버그 모드 + 전체 인터페이스에서 접근 허용
    app.run(host='0.0.0.0', port=5000, debug=True)

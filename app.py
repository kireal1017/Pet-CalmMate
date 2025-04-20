# app.py
from flask import Flask, jsonify, Response
from flask_cors import CORS
import time, cv2

# —————— 기존 블루프린트 import ——————
from routes.user import user_bp
from routes.dog import dog_bp

# —————— Paho MQTT (로컬/퍼블릭 브로커) ——————
import paho.mqtt.client as mqtt
MQTT_BROKER = "localhost"       # 로컬 mosquitto 쓰실 거면 localhost
# MQTT_BROKER = "test.mosquitto.org"  # 아니면 퍼블릭 브로커
MQTT_PORT   = 1883

mqtt_client = mqtt.Client(protocol=mqtt.MQTTv311)
try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
    print(f"[MQTT] Connected to {MQTT_BROKER}:{MQTT_PORT}")
except Exception as e:
    print(f"[MQTT] Connection failed: {e}")

# —————— Flask 셋업 ——————
app = Flask(__name__)
CORS(app)
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(dog_bp, url_prefix='/api')

# —————— 카메라 스트림 설정 ——————
camera_on     = False
video_capture = cv2.VideoCapture(0)

def gen_frames():
    global camera_on
    while True:
        if not camera_on:
            time.sleep(0.1)
            continue
        ok, frame = video_capture.read()
        if not ok: break
        _, buf = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')

# —————— API 라우트 ——————
@app.route('/api/stream')
def stream():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/camera/toggle', methods=['POST'])
def toggle_camera():
    global camera_on
    camera_on = not camera_on
    return jsonify({'camera_on': camera_on})

@app.route('/api/mic/toggle', methods=['POST'])
def toggle_mic():
    return jsonify({'mic_on': True})

@app.route('/api/dispense-snack', methods=['POST'])
def dispense_snack():
    try:
        mqtt_client.publish('pet/dispense', payload='SNACK', qos=1)
        return jsonify({'success': True, 'message': 'MQTT 간식 신호 발행 완료'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

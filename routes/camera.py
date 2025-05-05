# routes/camera.py
from flask import Blueprint, jsonify, Response
import time, cv2

camera_bp = Blueprint('camera', __name__)

camera_on     = False
video_capture = cv2.VideoCapture(0)

@camera_bp.route('/camera/toggle', methods=['POST'])
def toggle_camera():
    """카메라 On/Off 토글"""
    global camera_on
    camera_on = not camera_on
    return jsonify({'camera_on': camera_on})

def gen_frames():
    """MJPEG 비디오 스트림 제너레이터"""
    global camera_on
    while True:
        if not camera_on:
            time.sleep(0.1)
            continue
        ok, frame = video_capture.read()
        if not ok:
            break
        _, buf = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')

@camera_bp.route('/stream')
def stream():
    """실시간 비디오 스트림(MJPEG)"""
    return Response(
        gen_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

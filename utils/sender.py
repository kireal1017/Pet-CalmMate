import requests

FLASK_BACKEND_URL = "http://54.180.212.150/api/dog-sound"

def send_result_to_backend(device_id, sound_type, confidence, timestamp):
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "device_id": device_id,
        "timestamp": timestamp,
        "sound_type": sound_type,
        "confidence": confidence
    }

    try:
        response = requests.post(FLASK_BACKEND_URL, json=data)
        print("백엔드 전송 결과:", response.status_code)
    except Exception as e:
        print("백엔드 전송 실패:", e)

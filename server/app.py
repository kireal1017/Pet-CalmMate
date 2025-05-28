from fastapi import FastAPI, UploadFile, Form
import torch
import os
#from server.preprocess import preprocess_audio
from utils.sender import send_result_to_backend
from server.barknet_detector import detect_bark as is_dog_bark
from datetime import datetime
from model import analyze_emotion

app = FastAPI()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = DogSoundClassifierV2().to(device)
model.load_state_dict(torch.load("dog_sound_classifier_v2.pth", map_location=device))
model.eval()

class_names = ["Bark", "Growl", "Grunt"]

@app.post("/ai/predict")
async def predict(file: UploadFile, device_id: str = Form(...)):
    print("🔄 [DEBUG] Step 1: Audio file saving started")

    # 1. 오디오 저장
    with open("temp.wav", "wb") as f:
        f.write(await file.read())

    print("🔄 [DEBUG] Step 2: Audio file saved")

    # 🔹 업로드 시각 기록
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"⏰ [DEBUG] Audio received at: {upload_time}")

    # 2. 강아지 소리 감지
    is_bark, confidence = is_dog_bark("temp.wav")
    if not is_bark:
        print(f"🔹 [DEBUG] No dog bark detected (confidence: {confidence:.2f})")
        return {
            "result": "No dog bark detected",
            "confidence": confidence,
            "timestamp": upload_time
        }

    print("🔄 [DEBUG] Step 3: Bark detected")

    # 3. 전처리
    mfcc = preprocess_audio("temp.wav", device)
    print("🔄 [DEBUG] Step 4: Preprocessing completed")

    # 4. 분류
    try:
        with torch.no_grad():
            outputs = model(mfcc)
            pred = torch.argmax(outputs, dim=1).item()
            confidence = torch.softmax(outputs, dim=1).max().item()
        result = class_names[pred]
        print(f"🔄 [DEBUG] Step 5: Prediction done - {result} with confidence {confidence}")
    except Exception as e:
        print(f"🔴 [ERROR] Model inference failed: {e}")
        return {"result": "Model inference failed"}

    # 5. 결과 전송
    print(f"🔄 [DEBUG] Step 6: Sending to Flask - {result}")
    send_result_to_backend(device_id, result, confidence, upload_time)
    print("🔄 [DEBUG] Step 7: sender.py call completed")

    return {
        "result": result,
        "confidence": confidence,
        "timestamp": upload_time
    }


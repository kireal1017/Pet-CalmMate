from fastapi import FastAPI, UploadFile, Form
import torch
import os
from model import DogSoundClassifierV2
from server.preprocess import preprocess_audio
from utils.sender import send_result_to_backend
from barknet_detector import detect_bark as is_dog_bark

app = FastAPI()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = DogSoundClassifierV2().to(device)
model.load_state_dict(torch.load("dog_sound_classifier_v2.pth", map_location=device))
model.eval()

class_names = ["Bark", "Growl", "Grunt"]

@app.post("/ai/predict")
async def predict(file: UploadFile, device_id: str = Form(...)):
    # 1. 오디오 저장
    with open("temp.wav", "wb") as f:
        f.write(await file.read())

    # 2. 강아지 소리 감지
    is_bark, _ = is_dog_bark("temp.wav")
    if not is_bark:
        return {"result": "No dog bark detected"}

    # 3. 전처리
    mfcc = preprocess_audio("temp.wav", device)

    # 4. 분류
    with torch.no_grad():
        outputs = model(mfcc)
        pred = torch.argmax(outputs, dim=1).item()
        confidence = torch.softmax(outputs, dim=1).max().item()

    result = class_names[pred]

    # 5. 결과 전송
    send_result_to_backend(device_id, result, confidence)

    return {"result": result}

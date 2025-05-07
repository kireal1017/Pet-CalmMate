from fastapi import FastAPI, UploadFile, Form
import torch
import os
from model import DogSoundClassifierV2
from server.preprocess import preprocess_audio
from utils.sender import send_result_to_backend
from server.barknet_detector import detect_bark as is_dog_bark

app = FastAPI()

# 모델 로드
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = DogSoundClassifierV2().to(device)
model.load_state_dict(torch.load("dog_sound_classifier_v2.pth", map_location=device))
model.eval()

class_names = ["Bark", "Growl", "Grunt"]

@app.post("/predict")
async def predict(file: UploadFile, device_id: str = Form(...)):
    # 받은 파일 저장
    with open("temp.wav", "wb") as f:
        f.write(await file.read())

    # BarkNet으로 애완견 소리 유무 판단
    if not is_dog_bark("temp.wav"):
        print("No dog bark detected")   # 로그 출력
        os.remove("temp.wav")           # 불필요한 파일 삭제
        return {"result": "No dog bark detected"}

    # 애완견 소리일 경우 분석 진행
    mfcc = preprocess_audio("temp.wav", device)

    with torch.no_grad():
        outputs = model(mfcc)
        pred = torch.argmax(outputs, dim=1).item()
        confidence = torch.softmax(outputs, dim=1).max().item()

    result = class_names[pred]
    print("예측 결과:", result)

    # 결과 백엔드 전송 (주석처리 가능 → 필요 시 활성화)
    # send_result_to_backend(device_id, result, confidence)

    # 분석 후 파일 삭제
    os.remove("temp.wav")

    return {"result": result}

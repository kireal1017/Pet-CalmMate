from fastapi import FastAPI, UploadFile, Form
import torch
from model import DogSoundClassifierV2
from server.preprocess import preprocess_audio
from utils.sender import send_result_to_backend
from .barknet_detector import detect_bark as is_dog_bark

app = FastAPI()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = DogSoundClassifierV2().to(device)
model.load_state_dict(torch.load("dog_sound_classifier_v2.pth", map_location=device))
model.eval()

class_names = ["Bark", "Growl", "Grunt"]

@app.post("/predict")
async def predict(file: UploadFile, device_id: str = Form(...)):
    with open("temp.wav", "wb") as f:
        f.write(await file.read())

    # BarkNet을 사용하여 애완견 소리 유무 판단
    if not is_dog_bark("temp.wav"):
        return {"result": "No dog bark detected"}

    mfcc = preprocess_audio("temp.wav", device)

    with torch.no_grad():
        outputs = model(mfcc)
        pred = torch.argmax(outputs, dim=1).item()
        confidence = torch.softmax(outputs, dim=1).max().item()

    result = class_names[pred]
    print("예측 결과:", result)

    # 백엔드로 전송
    send_result_to_backend(device_id, result, confidence)

    return {"result": result}

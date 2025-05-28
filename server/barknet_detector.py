import os
import torch
import torchaudio
import torchaudio.transforms as T
from transformers import AutoProcessor, AutoModel
import torch.nn as nn

# 전역 설정
THRESHOLD = 0.1
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "whisper_dog_model.pth")


# Whisper 분류기 정의
class WhisperClassifier(nn.Module):
    def __init__(self, base_model, hidden_dim=768, num_labels=2):
        super().__init__()
        self.encoder = base_model.encoder
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim, 128),
            nn.ReLU(),
            nn.Linear(128, num_labels)
        )

    def forward(self, input_features):
        with torch.no_grad():
            features = self.encoder(input_features).last_hidden_state
        pooled = features.mean(dim=1)
        return self.classifier(pooled)

# Whisper 모델 및 Processor 로드
processor = AutoProcessor.from_pretrained("openai/whisper-small")
base_model = AutoModel.from_pretrained("openai/whisper-small")
model = WhisperClassifier(base_model).to(device)

# 저장된 학습 파라미터 로드
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()

# 전처리 함수
def preprocess_audio(path, silence_threshold=0.01):
    waveform, sr = torchaudio.load(path)
    waveform = waveform.mean(dim=0).unsqueeze(0)  # mono

    # 무음 필터
    if waveform.abs().mean().item() < silence_threshold:
        return None

    # 리샘플링
    if sr != 16000:
        waveform = T.Resample(orig_freq=sr, new_freq=16000)(waveform)

    # 정규화
    waveform = waveform / waveform.abs().max()

    # Whisper 입력
    inputs = processor(waveform.squeeze(), sampling_rate=16000, return_tensors="pt")
    return inputs["input_features"].squeeze(0).unsqueeze(0).to(device)

# 감지 함수: 입력 → 결과(True/False), confidence 반환
def detect_bark(file_path, threshold=0.1):
    try:
        input_features = preprocess_audio(file_path)
        if input_features is None:
            return False, 0.0

        with torch.no_grad():
            logits = model(input_features)
            probs = torch.softmax(logits, dim=1)[0]
            dog_prob = probs[1].item()

        return (dog_prob >= threshold), dog_prob

    except Exception:
        return False, 0.0

# CLI 테스트용
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("사용법: python barknet_detector.py <오디오파일경로>")
    else:
        result, conf = detect_bark(sys.argv[1])
        print("🗣️ 개가 짖었습니다!" if result else "🔇 짖지 않았습니다.", f"(신뢰도: {conf:.2f})")

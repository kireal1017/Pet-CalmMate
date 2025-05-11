from transformers import pipeline

# 1. 모델 초기화 (최초 한 번만 로드됨)
classifier = pipeline(
    "audio-classification",
    model="ardneebwar/wav2vec2-animal-sounds-finetuned-hubert-finetuned-animals"
)

# 2. 강아지 소리 감지 함수 정의
def detect_bark(file_path, threshold=0.85):
   
    try:
        # top_k=1 설정: 가장 가능성 높은 클래스만 추출
        results = classifier(file_path, top_k=1)
        label = results[0]["label"].lower()
        score = results[0]["score"]

        print(f"감지 라벨: {label}, 신뢰도: {score:.2f}")

        if label == "dog" and score >= threshold:
            return True, score
        else:
            return False, score
    except Exception as e:
        print("예외 발생 (detect_bark):", e)
        return False, 0.0

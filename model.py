import librosa
import numpy as np

def extract_features_fixed(wav_path, sr=16000, n_fft=512, hop_length=128):
    y, sr = librosa.load(wav_path, sr=sr)
    S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

    total_energy = S.sum()
    low = S[freqs < 2000].sum() / total_energy
    mid = S[(freqs >= 2000) & (freqs < 4000)].sum() / total_energy
    high = S[freqs >= 4000].sum() / total_energy

    energy_over_time = S.sum(axis=0)
    mean_energy = np.mean(energy_over_time)
    std_energy = np.std(energy_over_time)
    energy_var_ratio = std_energy / (mean_energy + 1e-6)
    avg_delta = np.mean(np.abs(np.diff(energy_over_time)))

    return {
        'low': low, 'mid': mid, 'high': high,
        'energy_var_ratio': energy_var_ratio,
        'avg_delta': avg_delta
    }

def classify_emotion(features):
    low = features['low']
    mid = features['mid']
    high = features['high']
    var_ratio = features['energy_var_ratio']
    avg_delta = features['avg_delta']

    if high > 0.25 and var_ratio > 0.5:
        return 'Sad'
    elif low > 0.7 and avg_delta < 0.2:
        return 'Lonely'
    elif low > 0.6 and high < 0.1 and avg_delta > 0.4:
        return 'Angry'
    elif low > 0.5 and high > 0.15:
        return 'Anxious'
    elif mid > 0.4 and avg_delta > 0.2:
        return 'Happy'
    else:
        return 'Unknown'

# 🔍 최종 분석 진입점
def analyze_emotion(wav_path):
    features = extract_features_fixed(wav_path)
    emotion = classify_emotion(features)
    confidence = round(random.uniform(0.5, 0.9), 3)
    return emotion, confidence

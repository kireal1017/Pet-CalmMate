import librosa
import noisereduce as nr
import numpy as np
import torch

def preprocess_audio(file_path, device):
    audio, sr = librosa.load(file_path, sr=16000)
    audio, _ = librosa.effects.trim(audio)

    samples = 16000 * 2
    if len(audio) < samples:
        audio = np.pad(audio, (0, samples - len(audio)))
    else:
        audio = audio[:samples]

    audio = nr.reduce_noise(y=audio, sr=sr)
    audio = librosa.util.normalize(audio)

    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    delta = librosa.feature.delta(mfcc)
    delta2 = librosa.feature.delta(mfcc, order=2)

    mfcc = np.concatenate([mfcc, delta, delta2], axis=0)

    mfcc = torch.tensor(mfcc).unsqueeze(0).unsqueeze(0).float().to(device)
    return mfcc

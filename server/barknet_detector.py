import torch
import torchaudio
from PIL import Image
import torchvision.transforms as transforms

class BarkDetectorCNN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = torch.nn.Sequential(
            torch.nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1),
            torch.nn.BatchNorm2d(16),
            torch.nn.ReLU(),
            torch.nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            torch.nn.BatchNorm2d(32),
            torch.nn.ReLU(),
            torch.nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            torch.nn.BatchNorm2d(64),
            torch.nn.ReLU(),
            torch.nn.AdaptiveAvgPool2d((1, 1))
        )
        self.fc = torch.nn.Linear(64, 1)

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BarkDetectorCNN().to(device)
model.load_state_dict(torch.load("dog_bark_cnn_optimized.pth", map_location=device))
model.eval()

def preprocess_audio(file_path, device):
    waveform, sr = torchaudio.load(file_path)
    samples = 16000 * 2
    if waveform.size(1) < samples:
        pad = samples - waveform.size(1)
        waveform = torch.nn.functional.pad(waveform, (0, pad))
    else:
        waveform = waveform[:, :samples]

    mel_spec = torchaudio.transforms.MelSpectrogram(sample_rate=16000, n_mels=64)(waveform)
    mel_spec_db = torchaudio.transforms.AmplitudeToDB()(mel_spec)

    transform = transforms.Compose([
        transforms.Resize((16, 16)),
        transforms.ToTensor()
    ])

    mel_spec_db = mel_spec_db.squeeze().cpu().numpy()
    image = Image.fromarray(mel_spec_db).convert("L")
    image_tensor = transform(image).unsqueeze(0).to(device)

    return image_tensor

def detect_bark(file_path):
    input_tensor = preprocess_audio(file_path, device)
    with torch.no_grad():
        output = model(input_tensor)
        prob = torch.sigmoid(output).item()

    if prob >= 0.5:
        return True, prob
    else:
        return False, prob

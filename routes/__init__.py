from .user import user_bp
from .dog import dog_bp
from .voice import voice_bp
from .device import device_bp  # 새로 만들 파일

__all__ = [
    "user_bp",
    "dog_bp",
    "voice_bp",
    "device_bp"
]

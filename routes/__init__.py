from .user import user_bp
from .dog import dog_bp
from .voice import voice_bp
from .device import device_bp
from .camera import camera_bp
from .mic import mic_bp
from .sound_data import sound_data_bp
# from .walk import walk_bp
# from .group import group_bp

# 블루프린트 리스트로 정리, app.py 가독성 증가를 위해 __init__에서 묶는다.
blueprints = [
    user_bp,
    dog_bp,
    voice_bp,
    device_bp,
    camera_bp,
    mic_bp,
    sound_data_bp,
    # walk_bp,
    # group_bp,
]
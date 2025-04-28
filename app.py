# app.py
from flask import Flask
from flask_cors import CORS

from routes.user   import user_bp
from routes.dog    import dog_bp
from routes.voice  import voice_bp
from routes.device import device_bp
from routes.camera import camera_bp
from routes.mic    import mic_bp
from routes.walk   import walk_bp

app = Flask(__name__)
CORS(app)

# URL Prefix 붙여서 등록
app.register_blueprint(user_bp,   url_prefix='/api')
app.register_blueprint(dog_bp,    url_prefix='/api')
app.register_blueprint(voice_bp,  url_prefix='/api')
app.register_blueprint(device_bp, url_prefix='/api')
app.register_blueprint(camera_bp, url_prefix='/api')
app.register_blueprint(mic_bp,    url_prefix='/api')
app.register_blueprint(walk_bp,  url_prefix='/api')

if __name__ == '__main__':
    # 0.0.0.0:5000 으로 바인딩 (외부 접속 허용)
    app.run(host='0.0.0.0', port=5000, debug=True)

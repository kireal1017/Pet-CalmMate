from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from db import db  # 추가
import time, cv2, os
from dotenv import load_dotenv
from routes.user   import user_bp
from routes.dog    import dog_bp
from routes.voice  import voice_bp
from routes.device import device_bp
from routes.camera import camera_bp
from routes.mic    import mic_bp
# from routes.walk   import walk_bp
# from routes.group  import group_bp

load_dotenv()  # .env 파일 불러오기

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

app = Flask(__name__)
CORS(app)

# SQLAlchemy 설정
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # 등록 필수

# 블루프린트 등록
app.register_blueprint(user_bp,   url_prefix='/api')
app.register_blueprint(dog_bp,    url_prefix='/api')
app.register_blueprint(voice_bp,  url_prefix='/api')
app.register_blueprint(device_bp, url_prefix='/api')
app.register_blueprint(camera_bp, url_prefix='/api')
app.register_blueprint(mic_bp,    url_prefix='/api')
#app.register_blueprint(walk_bp, url_prefix='/api')
#app.register_blueprint(group_bp,    url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
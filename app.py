from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from db import db 
import os, logging
from dotenv import load_dotenv
from config import SQLALCHEMY_DATABASE_URI
from config import JWT_SECRET_KEY,JWT_ACCESS_TOKEN_EXPIRES_DELTA
from routes import blueprints
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)

# SQLAlchemy 설정 (즉, RDS 데이터베이스로 설정)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # 등록 필수

# JWT 설정
# .env 에 JWT_SECRET_KEY 와 JWT_ACCESS_TOKEN_EXPIRES (초 단위) 를 추가해 둡니다.
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_ACCESS_TOKEN_EXPIRES_DELTA

# JWTManager 초기화
jwt = JWTManager(app)

# 블루프린트 등록
for bp in blueprints:
    app.register_blueprint(bp, url_prefix='/api')

#개발용 연결 확인 메인페이지
@app.route('/')
def home():
    return "Hello, Flask!"

# 🔄 로깅 설정
logging.basicConfig(
    filename='flask_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 🔄 모든 요청을 로깅
@app.before_request
def log_request_info():
    app.logger.info(f"Request Method: {request.method} | Path: {request.path} | IP: {request.remote_addr}")
    app.logger.info(f"Headers: {request.headers}")
    if request.method in ['POST', 'PUT', 'PATCH']:
        if request.content_type and 'application/json' in request.content_type:
            app.logger.info(f"Payload: {request.get_json()}")
        else:
            app.logger.info("Payload: [multipart/form-data or other]")


#시작
if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG", "True") == "True") #실제 배포 시에 .env에서 DEBUG=False로 바꾼다. False:실배포/운영, True:개발/테스트

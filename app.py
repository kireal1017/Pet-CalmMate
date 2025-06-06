import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES_DELTA
from db import db
from routes import blueprints
load_dotenv()

def create_app():
    app = Flask(__name__)

    # ── 1) 기본 설정 ───────────────────────────────────────────────────────────────
    # CORS 활성화
    CORS(app)

    # SQLAlchemy 설정 (예: RDS MySQL 또는 SQLite 등)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT 설정
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES_DELTA

    # ── 2) 확장 모듈 초기화 ───────────────────────────────────────────────────────
    # SQLAlchemy
    db.init_app(app)

    # Flask-Migrate 초기화
    migrate = Migrate(app, db)

    # JWTManager
    jwt = JWTManager(app)

    # ── 3) 블루프린트 등록 ───────────────────────────────────────────────────────
    # routes/__init__.py에서 정의된 blueprints 리스트를 순회하며 등록
    for bp in blueprints:
        # 모든 블루프린트는 '/api' 하위에 붙도록 설정하려면 url_prefix를 '/api'로 지정
        app.register_blueprint(bp, url_prefix='/api')

    # ── 4) 라우트 추가 (테스트용) ─────────────────────────────────────────────────
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({'message': 'Hello, Flask! 서버가 정상 작동 중입니다.'}), 200

    return app

# ────────────────────────────────────────────────────────────────────────────────
# 로깅 설정 (로그 파일: flask_app.log)
logging.basicConfig(
    filename='flask_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 모든 요청을 로그에 남깁니다.
# (POST, PUT, PATCH 요청 시 JSON 페이로드도 함께 기록)
def configure_logging(app):
    @app.before_request
    def log_request_info():
        app.logger.info(f"Request Method: {request.method} | Path: {request.path} | IP: {request.remote_addr}")
        app.logger.info(f"Headers: {dict(request.headers)}")
        if request.method in ['POST', 'PUT', 'PATCH']:
            if request.content_type and 'application/json' in request.content_type:
                app.logger.info(f"Payload: {request.get_json()}")
            else:
                app.logger.info("Payload: [multipart/form-data or other]")

if __name__ == '__main__':
    app = create_app()
    configure_logging(app)
    debug_mode = os.getenv("DEBUG", "True") == "True"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
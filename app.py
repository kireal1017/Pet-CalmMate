from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from db import db 
import os
from dotenv import load_dotenv
from config import SQLALCHEMY_DATABASE_URI
from routes import blueprints

app = Flask(__name__)
CORS(app)

# SQLAlchemy 설정 (즉, RDS 데이터베이스로 설정)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # 등록 필수

# 블루프린트 등록
for bp in blueprints:
    app.register_blueprint(bp, url_prefix='/api')

#개발용 연결 확인 메인페이지
@app.route('/')
def home():
    return "Hello, Flask!"

#시작
if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG", "True") == "True") #실제 배포 시에 .env에서 DEBUG=False로 바꾼다. False:실배포/운영, True:개발/테스트

import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# ── AWS S3 관련 설정 ─────────────────────────────────
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID") #반드시 .env에서 환경변수로 불러올 것, "절대 실제 키를 직접 입력하지 말 것"
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY") #반드시 .env에서 환경변수로 불러올 것, "절대 실제 키를 직접 입력하지 말 것"
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_S3_REGION = os.getenv("AWS_S3_REGION")

# ── DB 관련 설정 ─────────────────────────────────────
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}'

EC2_PUBLIC_IP = os.getenv("EC2_IP")
RTMP_STREAM_ID = os.getenv("RTMP_STREAM_ID")
HLS_BASE_URL = f"http://{EC2_PUBLIC_IP}/hls"

# JWT 설정정
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise RuntimeError("환경 변수 JWT_SECRET_KEY가 설정되지 않았습니다. 반드시 .env에 추가하세요.")

# 액세스 토큰 만료 시간(초 단위)
try:
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600"))
except ValueError:
    JWT_ACCESS_TOKEN_EXPIRES = 3600

JWT_ACCESS_TOKEN_EXPIRES_DELTA = timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRES)

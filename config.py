import os
from dotenv import load_dotenv

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
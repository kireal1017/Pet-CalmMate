# config.py
import os
from dotenv import load_dotenv

# .env 를 로드해서 민감정보를 가져옵니다
load_dotenv()

# —————— AWS S3 설정 ——————
AWS_ACCESS_KEY_ID     = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET_NAME    = os.getenv("AWS_S3_BUCKET_NAME")
AWS_S3_REGION         = os.getenv("AWS_S3_REGION")

# —————— MySQL (또는 MariaDB) 설정 ——————
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_USER     = os.getenv("DB_USER", "your_db_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_db_password")
DB_NAME     = os.getenv("DB_NAME", "petcalmmate")

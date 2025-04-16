import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID") #반드시 .env에서 환경변수로 불러올 것. 진짜 키를 작성하면 안됨됨
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY") #반드시 .env에서 환경변수로 불러올 것. 진짜 키를 작성하면 안됨됨
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_S3_REGION = os.getenv("AWS_S3_REGION")
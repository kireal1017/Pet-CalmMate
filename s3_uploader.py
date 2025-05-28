import boto3
import uuid
from config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_S3_BUCKET_NAME,
    AWS_S3_REGION
)
from botocore.exceptions import BotoCoreError, ClientError

def upload_file_to_s3(file_obj, filename, folder='uploads', max_size_mb=10):
    # 파일 크기 제한
    file_obj.seek(0, 2)  # 파일 끝으로 이동
    file_size = file_obj.tell()
    file_obj.seek(0)  # 다시 처음으로

    if file_size > max_size_mb * 1024 * 1024:
        raise ValueError(f"파일이 {max_size_mb}MB를 초과합니다.")

    # 고유 파일명 생성
    unique_filename = f"{folder}/{uuid.uuid4().hex}_{filename}"

    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_S3_REGION
        )

        s3.upload_fileobj(
            file_obj,
            AWS_S3_BUCKET_NAME,
            unique_filename,
            ExtraArgs={
                'ContentType': file_obj.content_type,
                #'ACL': 'public-read'  # 공개 URL 접근 허용
            }
        )

        return f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_S3_REGION}.amazonaws.com/{unique_filename}"

    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"S3 업로드 실패: {str(e)}")

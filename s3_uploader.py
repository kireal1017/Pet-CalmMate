import boto3
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET_NAME, AWS_S3_REGION
import uuid

def upload_file_to_s3(file_obj, filename, folder='uploads'):
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_S3_REGION)

    unique_filename = f"{folder}/{uuid.uuid4().hex}_{filename}"
    
    s3.upload_fileobj(file_obj, AWS_S3_BUCKET_NAME, unique_filename,
                      ExtraArgs={'ContentType': file_obj.content_type})
    
    return f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_S3_REGION}.amazonaws.com/{unique_filename}"
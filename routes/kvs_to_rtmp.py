import boto3
import subprocess

STREAM_NAME = "rpi-video"  # ← 여기를 바꿔야 해!
REGION = "ap-northeast-2"  # 서울 리전

print("🔍 Getting KVS endpoint...")
kvs_client = boto3.client("kinesisvideo", region_name=REGION)
endpoint = kvs_client.get_data_endpoint(
    StreamName=STREAM_NAME,
    APIName="GET_MEDIA"
)['DataEndpoint']

print("📡 Connecting to media stream...")
media_client = boto3.client("kinesis-video-media", endpoint_url=endpoint, region_name=REGION)
media_response = media_client.get_media(
    StreamName=STREAM_NAME,
    StartSelector={"StartSelectorType": "NOW"}
)

ffmpeg_command = [
    "ffmpeg",
    "-i", "pipe:0",
    "-c:v", "libx264",
    "-preset", "ultrafast",
    "-f", "flv",
    "rtmp://localhost:1935/live/kvs-stream"
]

print("🚀 Starting ffmpeg...")
process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

print("🎥 Streaming from KVS to ffmpeg...")
try:
    for chunk in media_response['Payload'].iter_chunks():
        process.stdin.write(chunk)
except KeyboardInterrupt:
    print("Stopped.")
    process.stdin.close()
    process.wait()
except Exception as e:
    print(f"Error: {e}")
    process.stdin.close()
    process.wait()

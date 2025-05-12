import os
import subprocess
from aws_privatekey import * # 예민한 정보는 별도 보관할 것 

# 스트리밍 엔드포인트와 키 분리
SERVER_URL = os.getenv('')
STREAM_KEY  = os.getenv('')


def start_ivs_stream():
    cmd = f"ffmpeg -f v4l2 -framerate 30 -video_size 640x480 -i /dev/video0 -c:v libx264 -preset veryfast -f flv {SERVER_URL}/{STREAM_KEY}"

    
    # subprocess에 리스트 형태 cmd 전달 (shell=False)
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    print(f"Started FFmpeg with PID {process.pid}")
    return process


def main():
    proc = start_ivs_stream()
    try:
        # 로그를 실시간으로 출력하며 ffmpeg 실행
        for line in proc.stdout:
            print(line, end='')
        proc.wait()
        print(f"FFmpeg exited with code {proc.returncode}")
    except KeyboardInterrupt:
        print("Stopping stream...")
        proc.terminate()
        proc.wait()
        print(f"Stream stopped with code {proc.returncode}")

if __name__ == '__main__':
    main()

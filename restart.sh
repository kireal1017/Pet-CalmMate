#!/bin/bash

echo "🔄 Gunicorn 재시작 중..."

# 🔄 Gunicorn 중지
pkill gunicorn

# 🔄 가상환경 활성화
source ~/Pet-CalmMate/venv/bin/activate

# 🔄 Gunicorn 백그라운드 실행
~/Pet-CalmMate/venv/bin/gunicorn app:app --bind 0.0.0.0:8000 --workers 1

# 🔄 실행 확인
if pgrep -x "gunicorn" > /dev/null
then
    echo "✅ Gunicorn이 정상적으로 실행되었습니다."
else
    echo "❌ Gunicorn 실행에 실패했습니다. 로그를 확인하세요."
    tail -n 20 ~/Pet-CalmMate/gunicorn.log
fi

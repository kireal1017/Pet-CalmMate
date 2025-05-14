#!/bin/bash

echo "🔄 Git에서 최신 코드 가져오는 중..."
cd ~/Pet-CalmMate

# Git Pull
git pull origin backend

# Pull 결과 확인
if [ $? -eq 0 ]; then
    echo "✅ Git Pull 완료!"
else
    echo "❌ Git Pull에 실패했습니다. 로그를 확인하세요."
    exit 1
fi

echo "🔄 Gunicorn 재시작 중..."
# Gunicorn 중지
pkill gunicorn

# Gunicorn 재시작
~/Pet-CalmMate/venv/bin/gunicorn app:app --bind 0.0.0.0:8000 --workers 1 --daemon

# 실행 확인
if pgrep -x "gunicorn" > /dev/null
then
    echo "✅ Gunicorn이 정상적으로 실행되었습니다."
else
    echo "❌ Gunicorn 실행에 실패했습니다."
fi


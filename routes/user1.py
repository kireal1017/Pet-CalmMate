import os
import re
import logging
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash
from db import get_connection
from utils.auth import token_required, create_jwt_token
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# 로깅 설정
logging.basicConfig(level=logging.INFO)

# 블루프린트 및 리미터 설정
user_bp = Blueprint('user', __name__, url_prefix='/api')
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(current_app)

# 이메일 형식 검증 정규식
_EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

# 📄 전체 사용자 조회 (관리자 권한 필요)
@user_bp.route('/users', methods=['GET'])
@token_required
def get_users(current_user_id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id, email, name FROM User ORDER BY id DESC")
            rows = cur.fetchall()
        return jsonify(rows), 200

    except Exception as e:
        logging.error(f"get_users error: {e}")
        return jsonify({'error': '서버 오류가 발생했습니다.'}), 500

# 🔑 카카오 소셜 로그인
@user_bp.route('/login/kakao', methods=['POST'])
@limiter.limit("10 per minute")
def kakao_login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    name = data.get('name', '').strip()

    # 입력값 검증
    if not email or not name:
        return jsonify({'error': '이메일과 이름을 모두 입력해주세요.'}), 400
    if not _EMAIL_REGEX.match(email):
        return jsonify({'error': '유효한 이메일 형식이 아닙니다.'}), 400

    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cur:
                # 기존 사용자 조회
                cur.execute("SELECT id, name FROM User WHERE email=%s", (email,))
                user = cur.fetchone()
                if not user:
                    # 신규 유저 생성
                    raw_pw = os.urandom(16).hex()
                    hashed = generate_password_hash(raw_pw, method='pbkdf2:sha256', salt_length=16)
                    cur.execute(
                        "INSERT INTO User (email, password, name) VALUES (%s, %s, %s)",
                        (email, hashed, name)
                    )
                    user_id = cur.lastrowid
                    user_name = name
                else:
                    user_id = user['id']
                    user_name = user['name']

        # JWT 토큰 발급
        token = create_jwt_token({'user_id': user_id})
        return jsonify({'token': token, 'email': email, 'name': user_name}), 200

    except Exception as e:
        logging.error(f"kakao_login error for {email}: {e}")
        return jsonify({'error': '서버 오류가 발생했습니다.'}), 500


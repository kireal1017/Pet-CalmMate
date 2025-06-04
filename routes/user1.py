import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db import db
from models import User
import logging

user_bp = Blueprint('user', __name__)

# 👤 유저 등록 API
@user_bp.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({'error': 'Invalid request format (JSON required)'}), 400

    data = request.get_json()
    required_fields = ['email', 'password', 'name']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    email = data['email']
    hashed_pw = generate_password_hash(data['password'])
    name = data['name']

    try:
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 409

        new_user = User(email=email, password=hashed_pw, name=name)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        logging.error(f"[User Register Error] {e}", exc_info=True)
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500


# 🔑 로그인 + 사용자 ID 반환 API
@user_bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'error': 'Invalid request format (JSON required)'}), 400

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid email or password'}), 401

        # JWT 대신 user_id만 반환
        return jsonify({'user_id': user.user_id}), 200
    except Exception as e:
        logging.error(f"[Login Error] {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


# 🔐 (예시) 보호된 API
# 이제는 JWT 없이 user_id로만 처리한다면, @jwt_required() 부분을 제거하거나
# 새로운 인증 로직(세션, 커스텀 헤더 등)에 맞게 바꿔야 합니다.
@user_bp.route('/profile', methods=['GET'])
# @jwt_required()
def protected_profile():
    # 예시: 클라이언트가 쿼리 파라미터나 헤더 등으로 user_id를 전달한다고 가정
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    try:
        user = User.query.get(user_id)
        if user:
            return jsonify({
                'user': {
                    'user_id': user.user_id,
                    'email': user.email,
                    'name': user.name
                }
            }), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        logging.error(f"[Protected API Error] {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

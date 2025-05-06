from flask import Blueprint, request, jsonify
from db import db
from models import User
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

user_bp = Blueprint('user', __name__)

# 👤 유저 등록 API (비밀번호 해싱 포함)
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    required_fields = ['email', 'password', 'name']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # 이메일 중복 확인
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    try:
        hashed_pw = generate_password_hash(data['password'])
        new_user = User(
            email=data['email'],
            password=hashed_pw,
            name=data['name']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully', 'user_id': new_user.user_id})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 📄 유저 전체 조회 API
@user_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([{
            'user_id': u.user_id,
            'email': u.email,
            'name': u.name
        } for u in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

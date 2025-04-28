import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Blueprint, jsonify, request
from db import get_connection

user_bp = Blueprint('user', __name__)

# 👤 유저 등록 API
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()  # 안전한 방식

    # 필수 입력값 확인
    required_fields = ['email', 'password', 'name']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cursor:
                sql = "INSERT INTO User (email, password, name) VALUES (%s, %s, %s)"
                cursor.execute(sql, (
                    data['email'],
                    data['password'],
                    data['name']
                ))
            conn.commit()
        return jsonify({'message': 'User created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 📄 유저 전체 조회 API
@user_bp.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM User")
                users = cursor.fetchall()
        return jsonify(users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

from flask import Blueprint, request, jsonify
from db import db
from models import Dog
from s3_uploader import upload_file_to_s3
from datetime import datetime
import uuid

dog_bp = Blueprint('dog', __name__)

# 🐶 강아지 등록 (사진 포함) API
@dog_bp.route('/dogs', methods=['POST'])
def add_dog():
    required_fields = ['user_id', 'name', 'breed', 'birth_date', 'gender']
    missing_fields = [field for field in required_fields if field not in request.form]

    if missing_fields:
        return jsonify({'error': f"Missing fields: {', '.join(missing_fields)}"}), 400

    if 'photo' not in request.files:
        return jsonify({'error': 'Missing photo file'}), 400

    try:
        birth_date = datetime.strptime(request.form['birth_date'], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'error': 'Invalid birth_date format (YYYY-MM-DD expected)'}), 400

    try:
        photo_file = request.files['photo']
        photo_url = upload_file_to_s3(photo_file, photo_file.filename, folder="dogs")

        new_dog = Dog(
            user_id=request.form['user_id'],
            name=request.form['name'],
            breed=request.form['breed'],
            birth_date=birth_date,
            gender=request.form['gender'],
            photo_url=photo_url
        )

        db.session.add(new_dog)
        db.session.commit()
        return jsonify({'message': 'Dog added successfully', 'dog_id': new_dog.dog_id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 🛠 강아지 수정 (사진 포함) API
@dog_bp.route('/dogs/<int:dog_id>', methods=['PUT'])
def update_dog(dog_id):
    required_fields = ['name', 'breed', 'birth_date', 'gender']
    missing_fields = [field for field in required_fields if field not in request.form]

    if missing_fields:
        return jsonify({'error': f"Missing fields: {', '.join(missing_fields)}"}), 400

    dog = db.session.get(Dog, dog_id)
    if not dog:
        return jsonify({'error': 'Dog not found'}), 404

    try:
        dog.name = request.form['name']
        dog.breed = request.form['breed']
        dog.birth_date = datetime.strptime(request.form['birth_date'], "%Y-%m-%d").date()
        dog.gender = request.form['gender']

        #사진이 전달된 경우에만 업데이트
        if 'photo' in request.files:
            photo_file = request.files['photo']
            dog.photo_url = upload_file_to_s3(photo_file, photo_file.filename, folder="dogs")

        db.session.commit()
        return jsonify({'message': 'Dog updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 📄 강아지 정보 조회 API (전체 또는 특정 유저)
@dog_bp.route('/dogs', methods=['GET'])
def get_dogs():
    user_id = request.args.get('user_id')
    try:
        query = Dog.query
        if user_id:
            query = query.filter_by(user_id=user_id)

        dogs = query.all()
        return jsonify([{
            'dog_id': dog.dog_id,
            'name': dog.name,
            'breed': dog.breed,
            'birth_date': dog.birth_date.isoformat(),
            'gender': dog.gender,
            'photo_url': dog.photo_url
        } for dog in dogs])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

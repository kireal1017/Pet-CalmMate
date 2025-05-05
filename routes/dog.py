from flask import Blueprint, request, jsonify
from db import db
from models import Dog
from s3_uploader import upload_file_to_s3

dog_bp = Blueprint('dog', __name__)

# 🐶 강아지 정보 등록 API
@dog_bp.route('/dogs', methods=['POST'])
def add_dog():
    data = request.get_json()
    required_fields = ['user_id', 'name', 'breed', 'birth_date', 'gender', 'photo_url']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_dog = Dog(**data)
    db.session.add(new_dog)
    db.session.commit()

    return jsonify({'message': 'Dog added successfully'})

# 🛠 강아지 정보 수정 API
@dog_bp.route('/dogs/<int:dog_id>', methods=['PUT'])
def update_dog(dog_id):
    data = request.get_json()
    required_fields = ['name', 'breed', 'birth_date', 'gender', 'photo_url']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    dog = Dog.query.get(dog_id)
    if not dog:
        return jsonify({'error': 'Dog not found'}), 404

    dog.name = data['name']
    dog.breed = data['breed']
    dog.birth_date = data['birth_date']
    dog.gender = data['gender']
    dog.photo_url = data['photo_url']

    try:
        db.session.commit()
        return jsonify({'message': 'Dog updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 📄 강아지 정보 전체 또는 사용자별 조회 API
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

# 🖼 S3 이미지 업로드 전용 API
@dog_bp.route('/dogs/photo-upload', methods=['POST'])
def upload_dog_photo():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    try:
        s3_url = upload_file_to_s3(file, file.filename)
        return jsonify({'s3_url': s3_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

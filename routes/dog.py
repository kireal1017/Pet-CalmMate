from flask import Blueprint, request, jsonify
from db import get_connection
from s3_uploader import upload_file_to_s3

dog_bp = Blueprint('dog', __name__)

# 🐶 강아지 정보 등록 API
@dog_bp.route('/dogs', methods=['POST'])
def add_dog():
    data = request.get_json()  # 더 안전한 방식

    # 필수 필드 존재 여부 확인
    required_fields = ['user_id', 'name', 'breed', 'birth_date', 'gender', 'photo_url']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO Dog (user_id, name, breed, birth_date, gender, photo_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    data['user_id'], data['name'], data['breed'],
                    data['birth_date'], data['gender'], data['photo_url']
                ))
            conn.commit()
        return jsonify({'message': 'Dog added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 🛠 강아지 정보 수정 API
@dog_bp.route('/dogs/<int:dog_id>', methods=['PUT'])
def update_dog(dog_id):
    data = request.get_json()
    required_fields = ['name', 'breed', 'birth_date', 'gender', 'photo_url']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE Dog SET
                        name = %s,
                        breed = %s,
                        birth_date = %s,
                        gender = %s,
                        photo_url = %s
                    WHERE dog_id = %s
                """
                cursor.execute(sql, (
                    data['name'], data['breed'],
                    data['birth_date'], data['gender'],
                    data['photo_url'], dog_id
                ))
            conn.commit()
        return jsonify({'message': 'Dog updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 📄 강아지 정보 전체 또는 사용자별 조회 API
@dog_bp.route('/dogs', methods=['GET'])
def get_dogs():
    user_id = request.args.get('user_id')  # ?user_id=5 쿼리 지원

    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cursor:
                if user_id:
                    cursor.execute("SELECT * FROM Dog WHERE user_id = %s", (user_id,))
                else:
                    cursor.execute("SELECT * FROM Dog")
                dogs = cursor.fetchall()
        return jsonify(dogs)
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

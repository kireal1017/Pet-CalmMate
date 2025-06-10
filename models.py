from db import db
from datetime import datetime

#실제 RDS 테이블 구조와 일치
class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    dogs = db.relationship('Dog', backref='owner', lazy=True)

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name


class Dog(db.Model):
    __tablename__ = 'Dog'
    dog_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum('M', 'F'), nullable=False)
    photo_url = db.Column(db.String(255))

    weight_records = db.relationship('WeightRecord', backref='dog', lazy=True)
    walk_records = db.relationship('WalkRecord', backref='dog', lazy=True)
    meals = db.relationship('Meal', backref='dog', lazy=True)
    sound_analyses = db.relationship('SoundAnalysis', backref='dog', lazy=True)

    def __init__(self, user_id, name, breed, birth_date, gender, photo_url=None):
        self.user_id = user_id
        self.name = name
        self.breed = breed
        self.birth_date = birth_date
        self.gender = gender
        self.photo_url = photo_url


class WeightRecord(db.Model):
    __tablename__ = 'WeightRecord'
    weight_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('Dog.dog_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Numeric(4, 1), nullable=False)

    def __init__(self, dog_id, date, weight):
        self.dog_id = dog_id
        self.date = date
        self.weight = weight


class WalkRecord(db.Model):
    __tablename__ = 'WalkRecord'
    walk_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('Dog.dog_id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    walk_distance = db.Column(db.Numeric(4, 1), nullable=False)
    walk_duration = db.Column(db.Integer, nullable=False)  # 단위: 초

    def __init__(self, dog_id, date_time, walk_distance, walk_duration):
        self.dog_id = dog_id
        self.date_time = date_time
        self.walk_distance = walk_distance
        self.walk_duration = walk_duration


class Meal(db.Model):
    __tablename__ = 'Meal'
    meal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('Dog.dog_id'), nullable=False)
    meal_datetime = db.Column(db.DateTime, nullable=False) 
    meal_amount = db.Column(db.String(50), nullable=False)
    memo = db.Column(db.String(255))

    def __init__(self, dog_id, meal_datetime, meal_amount, memo=None):
        self.dog_id = dog_id
        self.meal_datetime = meal_datetime
        self.meal_amount = meal_amount
        self.memo = memo



class SoundAnalysis(db.Model):
    __tablename__ = 'SoundAnalysis'
    analysis_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('Dog.dog_id'), nullable=False)
    record_date = db.Column(db.DateTime, nullable=False)
    anxiety_level = db.Column(db.Integer)
    sound_features = db.Column(db.String(255))

    def __init__(self, dog_id, record_date, anxiety_level, sound_features):
        self.dog_id = dog_id
        self.record_date = record_date
        self.anxiety_level = anxiety_level
        self.sound_features = sound_features
        

# 소리 감지 알림을 저장할 테이블
class SoundAlert(db.Model):
    __tablename__ = 'sound_alert'

    id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dog_id       = db.Column(db.Integer, nullable=False)            # 감지 대상 강아지 ID
    sound_level  = db.Column(db.Float, nullable=False)              # 감지된 소리 레벨 (데시벨 등)
    alert_time   = db.Column(db.DateTime, default=datetime.utcnow)  # 알림 발생 시각

    def __repr__(self):
        return f"<SoundAlert id={self.id} dog_id={self.dog_id} level={self.sound_level}>"


class ChatSolution(db.Model):
    __tablename__ = 'Chatsolution'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, prompt, answer, created_at):
        self.user_id = user_id
        self.prompt = prompt
        self.answer = answer
        self.created_at = created_at

class Device(db.Model):
    __tablename__ = 'Device'
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)  # PK
    device_id     = db.Column(db.String(100), unique=True, nullable=False)       # <- 실제 전송받는 값
    owner_id      = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=True)
    push_token    = db.Column(db.String(255), nullable=True)
    dog_id        = db.Column(db.Integer, db.ForeignKey('Dog.dog_id'), nullable=True)
    created_at    = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    def __init__(self, device_id, dog_id=None):
        self.device_id = device_id
        self.dog_id = dog_id

    def __repr__(self):
        return f"<Device device_id={self.device_id}, dog_id={self.dog_id}>"
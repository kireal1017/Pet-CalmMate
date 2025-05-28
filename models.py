from db import db

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

    care_records = db.relationship('CareRecord', backref='dog', lazy=True)
    meals = db.relationship('Meal', backref='dog', lazy=True)
    sound_analyses = db.relationship('SoundAnalysis', backref='dog', lazy=True)
    def __init__(self, user_id, name, breed, birth_date, gender, photo_url=None):
        self.user_id = user_id
        self.name = name
        self.breed = breed
        self.birth_date = birth_date
        self.gender = gender
        self.photo_url = photo_url

class CareRecord(db.Model):
    __tablename__ = 'CareRecord'
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('Dog.dog_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Numeric(4, 1))
    anxiety_level = db.Column(db.Integer)
    walk_distance = db.Column(db.Numeric(5, 2))


class Meal(db.Model):
    __tablename__ = 'Meal'
    meal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('Dog.dog_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    food_name = db.Column(db.String(100), nullable=False)
    meal_amount = db.Column(db.String(50), nullable=False)
    kcal = db.Column(db.Integer)
    memo = db.Column(db.String(255))
    def __init__(self, dog_id, date, weight=None, anxiety_level=None, walk_distance=None):
        self.dog_id = dog_id
        self.date = date
        self.weight = weight
        self.anxiety_level = anxiety_level
        self.walk_distance = walk_distance

class SoundAnalysis(db.Model):
    __tablename__ = 'SoundAnalysis'
    analysis_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('Dog.dog_id'), nullable=False)
    record_date = db.Column(db.DateTime, nullable=False)
    anxiety_level = db.Column(db.Integer)
    sound_features = db.Column(db.String(255))
    def __init__(self, dog_id, anxiety_level, sound_features):
        self.dog_id = dog_id
        self.anxiety_level = anxiety_level
        self.sound_features = sound_features

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
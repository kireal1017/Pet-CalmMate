from db import db

#실제 RDS 테이블 구조와 일치
class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    dogs = db.relationship('Dog', backref='owner', lazy=True)


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

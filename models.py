from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# SQLAlchemy 초기화
# app.py에서 db.init_app(app) 이후 create_all()을 호출합니다.
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # one-to-one 관계: User.dog으로 접근
    dog = db.relationship('Dog', uselist=False, back_populates='user')

class Dog(db.Model):
    __tablename__ = 'dog'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # User.dog과 매핑
    user = db.relationship('User', back_populates='dog')

class WalkRecord(db.Model):
    __tablename__ = 'walk_record'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    total_time = db.Column(db.Integer, default=0)
    total_distance = db.Column(db.Float, default=0.0)
    
    # User.walks로 리스트 접근 가능
    user = db.relationship('User', backref=db.backref('walks', lazy=True))
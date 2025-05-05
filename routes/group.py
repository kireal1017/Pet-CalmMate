'''# routes/group.py 에서 import 할 db, User 모델은 app.py 에 정의되어 있어야 합니다.
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db

group_bp = Blueprint('group', __name__)

# — Group 테이블: 그룹 기본 정보 (한 개의 강아지 그룹)
class Group(db.Model):
    __tablename__ = 'groups'
    id               = db.Column(db.Integer, primary_key=True)
    name             = db.Column(db.String(30), nullable=False)  # 그룹 이름
    dog_name         = db.Column(db.String(30), nullable=False)  # 강아지 이름
    dog_breed        = db.Column(db.String(30), nullable=False)  # 강아지 품종
    dog_birth_date   = db.Column(db.Date,   nullable=False)     # 강아지 생일 (YYYY-MM-DD)
    dog_gender       = db.Column(db.String(1), nullable=False)  # M/F 또는 '남'/'여'
    owner_id         = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)

    owner            = db.relationship('User', backref='owned_groups')

# — GroupMember 테이블: 그룹-유저 N:N 관계, 초대/참여자 관리
class GroupMember(db.Model):
    __tablename__ = 'group_members'
    id               = db.Column(db.Integer, primary_key=True)
    group_id         = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    user_id          = db.Column(db.Integer, db.ForeignKey('user.id'),   nullable=False)
    is_admin         = db.Column(db.Boolean, default=False)              # 그룹장 여부
    invited_at       = db.Column(db.DateTime, default=datetime.utcnow)

    group            = db.relationship('Group', backref=db.backref('members', lazy=True))
    user             = db.relationship('User',  backref=db.backref('groups', lazy=True))
'''
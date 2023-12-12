from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from app import db, login_manager

db = SQLAlchemy()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable=False)

    red_flags = db.relationship('RedFlag', backref='user', lazy=True)
    interventions = db.relationship('Intervention', backref='user', lazy=True)


class RedFlag(db.Model):
    __tablename__ = 'redflag'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    # location_lat = db.Column(db.Float, nullable=True)
    # location_long = db.Column(db.Float, nullable=True)
    location = db.Column(db.String(20), default='pending') 
    image_file = db.Column(db.String, nullable=False)
    video_file = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(255), nullable=False) #fix this
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)


class Intervention(db.Model):
    __tablename__ = 'intervention'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    # location_lat = db.Column(db.Float, nullable=True)
    # location_long = db.Column(db.Float, nullable=True)
    location = db.Column(db.String(20), default='pending') 
    image_file = db.Column(db.String, nullable=False)
    video_file = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    # first_name = db.Column(db.String(50), nullable=False)
    # last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    red_flags = db.relationship('RedFlag', backref='user', lazy=True)
    interventions = db.relationship('Intervention', backref='user', lazy=True)

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), default='user', nullable=False)

    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'


class UserProfile(db.Model):
    __tablename__ = 'users_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone_number = db.Column(db.String(80))
    user_photo = db.Column(db.String(255))
    user_age = db.Column(db.Integer)

    def __repr__(self):
        return f'<UserProfile {self.id}>'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        truncated_content = (self.content[:250] + '...') if len(self.content) > 200 else self.content
        return f'<Post {truncated_content}>'

    def get_formatted_created_at(self):
        return self.created_at.strftime("%d-%m-%Y %H:%M")

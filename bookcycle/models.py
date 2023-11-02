from datetime import datetime
from uuid import uuid4
from bookcycle import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def get_uuid():
    return uuid4().hex

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String(60), primary_key=True, unique=True, default=get_uuid)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)
    books = db.relationship('Book', backref='user', lazy=True)  # Change 'lazy=True' to 'lazy='dynamic'

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.String(60), primary_key=True, unique=True, default=get_uuid)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)  # Change 'user.id' to 'users.id'
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    book_image = db.Column(db.String(25), nullable=False, default='book_default.jpg')

    def __repr__(self):
        return f"Book({self.title}, {self.created_at})"
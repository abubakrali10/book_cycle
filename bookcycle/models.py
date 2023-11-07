from datetime import datetime
from uuid import uuid4
from bookcycle import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """
    Load a user based on their user ID.

    Args:
        user_id (str): The user's unique ID.

    Returns:
        User: The User object associated with the provided user ID.
    """
    return User.query.get(user_id)

def get_uuid():
    """
    Generate a random UUID as a hexadecimal string.

    Returns:
        str: A unique hexadecimal string generated as a UUID.
    """
    return uuid4().hex


class User(db.Model, UserMixin):
    """
    User model for representing registered users.

    Attributes:
        id (str): Unique user ID.
        username (str): User's username.
        email (str): User's email address.
        password (str): User's password.
        books (relationship): One-to-many relationship with Book model.
    """
    __tablename__ = 'users'
    id = db.Column(db.String(60), primary_key=True, unique=True, default=get_uuid)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)
    books = db.relationship('Book', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Book(db.Model):
    """
    Book model for representing books posted by users.

    Attributes:
        id (str): Unique book ID.
        user_id (str): ID of the user who posted the book.
        title (str): Title of the book.
        author (str): Author of the book.
        description (str): Description of the book.
        phone_number (str): Contact phone number for the book owner.
        created_at (datetime): Timestamp of when the book was created.
        book_image (str): File name of the book's image.
    """
    __tablename__ = 'books'
    id = db.Column(db.String(60), primary_key=True, unique=True, default=get_uuid)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    book_image = db.Column(db.String(25), nullable=False, default='book_default.jpg')

    def __repr__(self):
        return f"Book({self.title}, {self.created_at})"

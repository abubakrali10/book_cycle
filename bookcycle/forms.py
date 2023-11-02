from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bookcycle.models import User


class RegistrationForm(FlaskForm):
    """
    Form for user registration.

    Attributes:
    - username (StringField): User's desired username.
    - email (StringField): User's email address.
    - password (PasswordField): User's password.
    - submit (SubmitField): Submit button for registration.
    """

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=25)])
    password_confirm = PasswordField(validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already exists!')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already exists!')


class LoginForm(FlaskForm):
    """
    Form for user login.

    Attributes:
    - email (StringField): User's email address.
    - password (PasswordField): User's password.
    - submit (SubmitField): Submit button for login.
    """

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=25)])
    submit = SubmitField('Log In')


class AddBookForm(FlaskForm):
    """
    Form for adding a new book.

    Attributes:
    - book_title (StringField): Title for the new book.
    - book_author (StringField): Author for the new book.
    - contact_number (StringField): Book Owner Phone number.
    - book_desc (StringField): Book's Description
    - book_image (FileField): Book's Image
    - submit (SubmitField): Submit button for book adding.
    """
    book_title = StringField('Book Title', validators=[DataRequired(), Length(max=255)])
    book_author = StringField('Book Author', validators=[DataRequired(), Length(max=255)])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])
    book_desc = TextAreaField('Book Description', validators=[DataRequired()])
    book_image = FileField('Book Image', validators=[DataRequired()])
    submit = SubmitField('Add')
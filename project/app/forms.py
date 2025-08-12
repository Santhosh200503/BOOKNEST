# app/forms.py

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, FileField, BooleanField
)
from wtforms.validators import (
    InputRequired, Email, EqualTo, DataRequired, Length
)
from flask_wtf.file import FileAllowed, FileRequired


# ------------------------------
# User Registration Form
# ------------------------------
class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="Username is required."),
            Length(min=3, max=150, message="Username must be between 3 and 150 characters.")
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please enter a valid email address.")
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required."),
            Length(min=6, message="Password must be at least 6 characters.")
        ]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message="Please confirm your password."),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    accept_terms = BooleanField(
        'I agree to the Terms & Conditions',
        validators=[DataRequired(message="You must accept the Terms & Conditions.")]
    )

    submit = SubmitField('Register')


# ------------------------------
# Login Form
# ------------------------------
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')  # ✅ Add this
    submit = SubmitField('Login')

# ------------------------------
# Upload  Form
# ------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import InputRequired

class UploadForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    author = StringField('Author', validators=[InputRequired()])
    genre = SelectField('Genre', choices=[
        ('', '-- Select Genre --'),
        ('fiction', 'Fiction'),
        ('nonfiction', 'Non-fiction'),
        ('romance', 'Romance'),
        ('mystery', 'Mystery'),
        ('fantasy', 'Fantasy'),
        ('biography', 'Biography')
    ], validators=[InputRequired()])
    description = TextAreaField('Description')
    cover = FileField('Cover Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    pdf_file = FileField('PDF File', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDF files only!')
    ])

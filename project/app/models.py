# models.py

from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    """
    User model for authentication and account management.
    """
    __tablename__ = 'users'  # Consistent table name
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=True)
    def __repr__(self):
        return f"<User id={self.id} username='{self.username}'>"


class Book(db.Model):
    """
    Book model to store uploaded e-books.
    """
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    #genre = db.Column(db.String(50), nullable=False)
    cover_filename = db.Column(db.String(200), nullable=False)
    pdf_filename = db.Column(db.String(200), nullable=False)
    

    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploader = db.relationship('User', backref='uploaded_books')




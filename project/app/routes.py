import os
from flask import (
    Blueprint, render_template, redirect, url_for,
    request, flash, send_file, abort, current_app
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from . import db, login_manager, bcrypt
from .models import User, Book
from .forms import RegisterForm, LoginForm, UploadForm

# --------------------------
# Blueprint
# --------------------------
main = Blueprint('main', __name__)

# --------------------------
# Flask-Login User Loader
# --------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --------------------------
# Admin-only Decorator
# --------------------------
def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# --------------------------
# Home Page
# --------------------------
@main.route('/', )
def home():
    query = request.args.get('q',) 
    books = [] # 'q' will be the search term from the form
    if query:
        books = Book.query.filter(Book.title.ilike(f'%{query}%')).all()
    
        
    return render_template('home.html', books=books)

# --------------------------
# Register
# --------------------------
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered.", "danger")
            return redirect(url_for('main.register'))

        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

# --------------------------
# Login
# --------------------------
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)

# --------------------------
# Logout
# --------------------------
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

# --------------------------
# Upload Book (Admin Only)
# --------------------------
@main.route('/upload', methods=['GET', 'POST'])
@admin_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        # Save cover
        cover = form.cover.data
        cover_filename = secure_filename(cover.filename)
        cover_path = os.path.join(current_app.config['UPLOAD_FOLDER_COVERS'], cover_filename)
        cover.save(cover_path)

        # Save PDF
        pdf = form.pdf_file.data
        pdf_filename = secure_filename(pdf.filename)
        pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER_PDFS'], pdf_filename)
        pdf.save(pdf_path)

        # Create book record
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            description=form.description.data,
            cover_filename=cover_filename,
            pdf_filename=pdf_filename,
            uploader_id=current_user.id
        )
        db.session.add(new_book)
        db.session.commit()

        flash('Book uploaded successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('upload.html', form=form)

# --------------------------
# All Books
# --------------------------
@main.route("/books", methods=["GET"])
@login_required
def all_books():
    query = request.args.get("q", "").strip()
    books = []
    popup_message = None  # message to show in modal

    if not current_user.is_authenticated:
        popup_message = "Please log in to view the books."
    else:
        books_query = Book.query
        if query:
            books_query = books_query.filter(Book.title.ilike(f"%{query}%"))
        books = books_query.all()

    return render_template(
        "books.html",
        books=books,
        query=query,
        popup_message=popup_message
    )

# --------------------------
# Book View Page
# --------------------------
from flask import flash, redirect, url_for, render_template
from flask_login import current_user

@main.route("/book/<int:book_id>")
def view_book(book_id):
    if not current_user.is_authenticated:
        # Show popup on home page if not logged in
        return render_template("home.html", show_login_popup=True)

    # Get book from DB or show 404 if not found
    book = Book.query.get_or_404(book_id)

    return render_template("book_view.html", book=book)


# --------------------------
# Download PDF
# --------------------------
@main.route('/download/<int:book_id>')
def download_pdf(book_id):
    book = Book.query.get_or_404(book_id)
    pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER_PDFS'], book.pdf_filename)
    if not os.path.exists(pdf_path):
        abort(404, description=f"PDF file not found: {book.pdf_filename}")
    return send_file(pdf_path, as_attachment=True)

# --------------------------
# Debug Route
# --------------------------
@main.route('/debug/books')
def debug_books():
    books = Book.query.all()
    return '<br>'.join([f"{book.id}: {book.title} by {book.author}" for book in books])

# --------------------------
# Delete Book (Admin Only)
# --------------------------
@main.route('/delete/<int:book_id>', methods=['POST'])
@admin_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    # Delete files
    if book.cover_filename:
        cover_path = os.path.join(current_app.config['UPLOAD_FOLDER_COVERS'], book.cover_filename)
        if os.path.exists(cover_path):
            os.remove(cover_path)

    if book.pdf_filename:
        pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER_PDFS'], book.pdf_filename)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully.', 'success')
    return redirect(url_for('main.home'))

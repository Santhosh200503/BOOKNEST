from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import os

# ===== Initialize extensions (single instances only) =====
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    """Flask application factory."""
    app = Flask(__name__)

    # ===== Basic Configurations =====
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
        os.path.dirname(BASE_DIR), 'ebooks.db'  # store DB at project root
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ===== Upload folders =====
    app.config['UPLOAD_FOLDER_COVERS'] = os.path.join(BASE_DIR, 'static', 'covers')
    app.config['UPLOAD_FOLDER_PDFS'] = os.path.join(BASE_DIR, 'static', 'books')
    os.makedirs(app.config['UPLOAD_FOLDER_COVERS'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER_PDFS'], exist_ok=True)

    # ===== Initialize Extensions with app =====
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Flask-Login settings
    login_manager.login_view = 'main.login'
    login_manager.login_message = "Please log in to upload books."

    # ===== Register Blueprints =====
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
from flask_login import current_user


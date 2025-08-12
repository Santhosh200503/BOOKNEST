from app import create_app, db
from flask_migrate import Migrate
from flask.cli import FlaskGroup
from app.models import User, Book
app = create_app()
migrate = Migrate(app, db)
cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()

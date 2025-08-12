# create_db.py

import os
from app import create_app, db

def create_database():
    """Create all database tables using the Flask app context."""
    app = create_app()
    db_path = os.path.join(os.path.abspath(os.getcwd()), 'ebooks.db')

    with app.app_context():
        if os.path.exists(db_path):
            print(f"ℹ️ Database already exists at: {db_path}")
        else:
            try:
                db.create_all()
                print(f"✅ Database created successfully at: {db_path}")
            except Exception as e:
                print("❌ Error creating database:")
                print(e)

if __name__ == "__main__":
    create_database()

# debug_users.py


# This script is a development/debugging utility for the SmartBite Flask application.
# It allows developers to view all registered users currently stored in the SQLite database.
# This is especially useful during development to verify that user registration is functioning correctly.

from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    users = User.query.all()
    for u in users:
        print(f"Username: {u.username}, Hash: {u.password_hash}, Salt: {u.salt}")

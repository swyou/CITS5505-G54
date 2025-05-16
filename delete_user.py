# This script is a development tool designed to allow developers to manually delete a user
# from the SQLite database used in the SmartBite Flask application.
# It is useful during testing or debugging when you need to remove test users from the system.

from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    username = input("Enter username to delete: ")
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        print(f"✅ User '{username}' deleted.")
    else:
        print(f"❌ User '{username}' not found.")

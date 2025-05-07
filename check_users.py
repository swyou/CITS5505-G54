# debug_users.py
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    users = User.query.all()
    for u in users:
        print(f"Username: {u.username}, Hash: {u.password_hash}, Salt: {u.salt}")

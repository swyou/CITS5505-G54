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

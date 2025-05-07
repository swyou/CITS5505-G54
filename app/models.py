from flask_login import UserMixin
# models.py
from . import db  # ✅ 从当前包中导入 db（db 定义在 app/__init__.py）


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    salt = db.Column(db.String(64), nullable=False)

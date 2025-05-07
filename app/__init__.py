# app/__init__.py

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # 导入模型 & 蓝图
    from .models import User
    from .auth import auth_bp
    from .routes import main
    app.register_blueprint(auth_bp)
    app.register_blueprint(main)

    # 用户加载函数
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    return app

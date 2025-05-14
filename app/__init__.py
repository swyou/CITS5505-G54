# app/__init__.py
import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()

# Load variables from .env into system environment
load_dotenv()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "UWA_CITS5505_G54_UYCOOS09V")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///foodie.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = \
        os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", "false").lower() == "true"
    app.config['DEBUG'] = os.environ.get("DEBUG", "false").lower() == "true"

    # init extentiosn
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # register blue prints
    from .models import User
    from .auth import auth_bp
    from .routes import main
    app.register_blueprint(auth_bp)
    app.register_blueprint(main)

    # load users function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    return app

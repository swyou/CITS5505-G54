# app/__init__.py
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config)

    # init extentiosn
    db.init_app(app)
    migrate.init_app(app, db)
    
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

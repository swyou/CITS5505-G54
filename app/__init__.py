# app/__init__.py

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user

# Initialize Flask extensions (to be bound to app later)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config):
    """
    Application factory function to create and configure the Flask app.
    """
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Flask-Login config
    login_manager.login_view = 'auth.login'  # Redirect here if not logged in

    # Import models (required for user_loader)
    from .models import User

    # Register blueprints
    from .auth import auth_bp
    from .routes import main
    app.register_blueprint(auth_bp)
    app.register_blueprint(main)

    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

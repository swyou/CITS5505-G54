from flask_login import UserMixin
# models.py
from . import db  


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    salt = db.Column(db.String(64), nullable=False)



class Sharing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User who shares the information
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User who receives the information
    shared_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())  # Timestamp of sharing
    message = db.Column(db.String(500), nullable=True)  # Optional message or description of the shared information

    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_shares')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_shares')

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)  # Name of the recipe
    servings = db.Column(db.Integer, nullable=False)  # Number of servings
    total_kcal = db.Column(db.Float, nullable=False)  # Total calories for the recipe
    kcal_per_serving = db.Column(db.Float, nullable=False)  # Calories per serving
    ingredients = db.Column(db.Text, nullable=False)  # Ingredients stored as a JSON string
    veg_g = db.Column(db.Float, nullable=False, default=0.0)  # Total grams of vegetables
    meat_g = db.Column(db.Float, nullable=False, default=0.0)  # Total grams of meat
    total_g = db.Column(db.Float, nullable=False, default=0.0)  # Total grams of all ingredients
    protein_g = db.Column(db.Float, nullable=False, default=0.0)  # Total grams of protein
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())  # Timestamp of creation

    # Foreign key to associate the recipe with a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


from flask_login import UserMixin
from . import db


# --------------------------
# User Model
# --------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for the user
    username = db.Column(db.String(150), unique=True, nullable=False)  # Unique username
    password_hash = db.Column(db.String(256), nullable=False)  # Hashed password
    salt = db.Column(db.String(64), nullable=False)  # Salt used for hashing


# --------------------------
# Sharing Model
# --------------------------
class Sharing(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for the sharing record

    # Foreign keys linking sender and receiver to the User table
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # The user who shares the data
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # The user who receives the data

    shared_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())  # Time of sharing
    message = db.Column(db.String(500), nullable=True)  # Optional message included in the share

    # Relationships to access sender and receiver User objects
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_shares')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_shares')


# --------------------------
# Recipe Model
# --------------------------
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique recipe ID
    name = db.Column(db.String(150), nullable=False)  # Recipe name
    servings = db.Column(db.Integer, nullable=False)  # Number of servings
    total_kcal = db.Column(db.Float, nullable=False)  # Total calories for the full recipe
    kcal_per_serving = db.Column(db.Float, nullable=False)  # Calories per individual serving

    ingredients = db.Column(db.Text, nullable=False)  # Ingredient data stored as JSON string

    veg_g = db.Column(db.Float, nullable=False, default=0.0)  # Total grams of vegetables
    meat_g = db.Column(db.Float, nullable=False, default=0.0)  # Total grams of meat
    total_g = db.Column(db.Float, nullable=False, default=0.0)  # Total grams of all ingredients
    protein_g = db.Column(db.Float, nullable=False, default=0.0)  # Total grams of protein

    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())  # Time of recipe creation

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to the user who created this recipe


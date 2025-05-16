from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
import os, hashlib
from . import db
from .models import User
from .forms import LoginForm, RegisterForm

# Create a blueprint for authentication-related routes
auth_bp = Blueprint('auth', __name__)

# Generate a random salt for password hashing
def generate_salt():
    return os.urandom(16).hex()


# ---------------------------
# Login Route
# ---------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = check_login(form.username.data, form.password.data)
        if user is not None:
            flash("Login successful!", "success")
            login_user(user)  # Log the user in
            return redirect(url_for('main.intro'))  # Redirect to main intro page
        flash("Invalid username or password.", category="login")  # Invalid credentials
    return render_template('login.html', form=form, show_register=False)


# ---------------------------
# Register Route
# ---------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Additional validation: confirm password must match
        password = form.password.data
        confirm = request.form.get('confirm_password')
        if password != confirm:
            flash("Passwords do not match.", category="register")
            return render_template('login.html', form=form, show_register=True)
        
        # Attempt to create user
        if creat_user(form.username.data, password):
            flash("Registration successful. Please login.", "success")
            return redirect(url_for('auth.login'))
        
        # If username already exists
        flash("Username already exists.", category="register")
    else:
        # Form validation failed (e.g. length constraints)
        print("❌ Register form errors:", form.errors)
        flash("Registration failed. Please ensure the username >= 3 characters and the password >= 6 characters.", category="register")

    return render_template('login.html', form=form, show_register=True)


# ---------------------------
# Helper Function: Create User
# ---------------------------
def creat_user(username, password):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return False  # Username is already taken
    salt = generate_salt()
    hash_pw = hashlib.sha256((password + salt).encode()).hexdigest()
    new_user = User(username=username, password_hash=hash_pw, salt=salt)
    db.session.add(new_user)
    db.session.commit()
    return True


# ---------------------------
# Helper Function: Check Credentials
# ---------------------------
def check_login(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        salted_input = password + user.salt
        input_hash = hashlib.sha256(salted_input.encode()).hexdigest()
        if input_hash == user.password_hash:
            return user  # Credentials match
    return None  # Invalid credentials


# ---------------------------
# Logout Route
# ---------------------------
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))  # Redirect to login page after logout

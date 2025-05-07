from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
import os, hashlib
from . import db
from .models import User
from .forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)

def generate_salt():
    return os.urandom(16).hex()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            salted_input = form.password.data + user.salt
            input_hash = hashlib.sha256(salted_input.encode()).hexdigest()
            if input_hash == user.password_hash:
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for('auth.intro'))
        flash("Invalid username or password.", category="login")
    return render_template('login.html', form=form, show_register=False)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 额外验证：密码和确认密码是否一致
        password = form.password.data
        confirm = request.form.get('confirm_password')
        if password != confirm:
            flash("Passwords do not match.", category="register")
            return render_template('login.html', form=form, show_register=True)
        
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already exists.", category="register")
        else:
            salt = generate_salt()
            hash_pw = hashlib.sha256((password + salt).encode()).hexdigest()
            new_user = User(username=form.username.data, password_hash=hash_pw, salt=salt)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful. Please login.", "success")
            return redirect(url_for('auth.login'))
    else:
        print("❌ Register form errors:", form.errors)
        flash("Registration failed. Please ensure the username >= 3 characters and the password >= 6 characters.", category="register")


    return render_template('login.html', form=form, show_register=True)

@auth_bp.route('/intro')
@login_required
def intro():
    return render_template('intro.html', username=current_user.username)


@auth_bp.route('/data')
@login_required
def data():
    return render_template('data.html', username=current_user.username)

@auth_bp.route('/share')
@login_required
def share():
    return render_template('share.html', username=current_user.username)

@auth_bp.route('/upload')
@login_required
def upload():
    return render_template('upload.html', username=current_user.username)



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

main = Blueprint("main", __name__)

@main.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.intro'))
    return redirect(url_for('auth.login'))


@main.route('/intro')
@login_required
def intro():
    return render_template('intro.html', username=current_user.username)


@main.route('/data')
@login_required
def data():
    return render_template('data.html', username=current_user.username)

@main.route('/share')
@login_required
def share():
    return render_template('share.html', username=current_user.username)

@main.route('/upload')
@login_required
def upload():
    return render_template('upload.html', username=current_user.username)
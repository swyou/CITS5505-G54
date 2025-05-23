from flask import Blueprint, jsonify, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .service import *
from .forms import RecipeForm, ShareDataForm

main = Blueprint('main', __name__)

@main.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.intro'))
    return redirect(url_for('auth.login'))


@main.route('/intro')
@login_required
def intro():
    return render_template('intro.html')


@main.route('/data')
@login_required
def data():
    return render_template('data.html', username=current_user.username)

@main.route('/share', methods=['GET', 'POST'])
@login_required
def share():
    form = ShareDataForm()
    
    # Populate the user dropdown
    user_id = current_user.get_id()
    users = [{"id": user.id, "username": user.username} for user in get_all_users_except_self(user_id)]
    form.user.choices = [(user['id'], user['username']) for user in users]

    if form.validate_on_submit():
        to_user_id = form.user.data
        user_id = current_user.get_id()

        # Check if a sharing already exists
        existing_sharing = get_existing_sharing(sender_id=user_id, receiver_id=to_user_id)
        if existing_sharing:
            flash('You have already shared data with this user.', 'warning')
        else:
            # Create a new sharing
            create_sharing(sender_id=user_id, receiver_id=to_user_id, message="")
            flash('Data shared successfully!', 'success')

    return render_template('share.html', form=form, username=current_user.username)

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = RecipeForm()

    if form.validate_on_submit():
        title = form.title.data
        servings = form.servings.data or 1
        date = form.date.data
        user_id = current_user.get_id()
        types = form.ingredient_type.data
        grams_choices = form.ingredient_grams.data
        grams_customs = form.ingredient_grams_custom.data
        # user_id, title, date, servings, types, grams_choices, grams_customs
        save_recipe(user_id, title, date, servings, types, grams_choices, grams_customs)

        flash('Recipe uploaded successfully!', 'success')
    elif form.is_submitted():

        flash('Failed to upload recipe. Please check your input.', 'danger')

    return render_template('upload.html', form=form, username=current_user.username)

@main.route('/sharings', methods=['GET'])
@login_required
def list_sharings():
    user_id = current_user.get_id()
    sharings = get_sharings_by_receiver(user_id)
    result = [
        {
            "id": sharing.id,
            "sender": sharing.sender.username
        }
        for sharing in sharings
    ]
    return jsonify(result)


@main.route('/users', methods=['GET'])
@login_required
def list_users():
    user_id = current_user.get_id()
    # remove credential information, only returns name and id.
    users = [{"id": user.id, "username": user.username} for user in get_all_users_except_self(user_id)]
    return jsonify(users)


@main.route('/analytics/daily_calories', methods=['GET'])
@login_required
def get_daily_calories():
    """
    Endpoint to get daily calories (one serving) for the last 7 days.
    """
    user_id = get_user_id_from_request()
    if user_id is None:
        return jsonify({"error": "Invalid sharing ID"}), 400

    data = daily_calories_one_serving(user_id)
    return jsonify(data)


@main.route('/analytics/veg_meat_proportion', methods=['GET'])
@login_required
def get_veg_meat_proportion():
    """
    Endpoint to get the proportion of vegetables and meat for the last 7 days.
    """
    user_id = get_user_id_from_request()
    if user_id is None:
        return jsonify({"error": "Invalid sharing ID"}), 400
    
    data = proportion_of_veg_and_meat(user_id)
    return jsonify(data)


@main.route('/analytics/daily_grams', methods=['GET'])
@login_required
def get_daily_grams():
    """
    Endpoint to get daily grams of food (one serving) for the last 7 days.
    """
    user_id = get_user_id_from_request()
    if user_id is None:
        return jsonify({"error": "Invalid sharing ID"}), 400

    data = daily_grams_of_food_one_serving(user_id)
    return jsonify(data)


@main.route('/analytics/daily_protein', methods=['GET'])
@login_required
def get_daily_protein():
    """
    Endpoint to get daily protein (one serving) for the last 7 days.
    """
    user_id = get_user_id_from_request()
    if user_id is None:
        return jsonify({"error": "Invalid sharing ID"}), 400

    data = daily_protein_one_serving(user_id)
    return jsonify(data)


def get_user_id_from_request():
    """
    Retrieve the user ID based on the request.
    If a sharing_id is provided, return the sender's user ID.
    Otherwise, return the current user's ID.

    :return: The user ID or None if the sharing_id is invalid.
    """
    sharing_id = request.args.get("sharing_id")
    if sharing_id:
        user_id = get_sender_id_by_sharing_id(sharing_id)
        if not user_id:
            return None  # Invalid sharing_id
        return user_id
    return current_user.get_id()



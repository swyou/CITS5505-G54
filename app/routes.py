from flask import Blueprint, jsonify, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .service import *
from .forms import RecipeForm

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

@main.route('/share')
@login_required
def share():
    return render_template('share.html', username=current_user.username)

@main.route('/upload', methods=['GET'])
@login_required
def upload():
    form = RecipeForm()
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


@main.route('/share_data', methods=['POST'])
@login_required
def share_with():
    data = request.get_json()  # Parse JSON payload
    to_user_id = data.get("to_user_id")
    if to_user_id is None:
        return jsonify({"error": "Invalid to user ID"}), 400

    user_id = current_user.get_id()
    # Check if a sharing already exists
    existing_sharing = get_existing_sharing(sender_id=user_id, receiver_id=to_user_id)
    if existing_sharing:
        return jsonify({"exist": True}), 201

    # Create a new sharing
    sharing = create_sharing(sender_id=user_id, receiver_id=to_user_id, message="")

    return jsonify({"success": True}), 201


@main.route('/upload_data', methods=['POST'])
@login_required
def handle_upload():
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
        return jsonify({"success": True}), 201
    else:
        return jsonify({"error": "Invalid form data"}), 400


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



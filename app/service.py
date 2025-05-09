from datetime import datetime, timedelta
from sqlalchemy import func
from app.models import Sharing, User, Recipe
from app import db
import json


def get_sharings_by_receiver(receiver_id):
    """
    List all sharings for a specific receiver.

    :param receiver_id: The ID of the user who is the receiver.
    :return: A list of sharing records.
    """
    sharings = Sharing.query.filter_by(receiver_id=receiver_id).all()
    return sharings


def get_all_users_except_self(user_id):
    """
    List all users except the one with the given user_id.

    :param user_id: The ID of the user to exclude.
    :return: A list of user records.
    """
    users = User.query.filter(User.id != user_id).all()
    return users


def create_sharing(sender_id, receiver_id, message):
    """
    Create a new sharing record.

    :param sender_id: The ID of the user who is the sender.
    :param receiver_id: The ID of the user who is the receiver.
    :return: The created sharing record.
    """
    new_sharing = Sharing(sender_id=sender_id, receiver_id=receiver_id, message=message)
    db.session.add(new_sharing)
    db.session.commit()
    return new_sharing


def get_existing_sharing(sender_id, receiver_id):
    """
    Check if a sharing already exists between the sender and receiver.

    :param sender_id: The ID of the sender.
    :param receiver_id: The ID of the receiver.
    :return: The existing sharing if found, otherwise None.
    """
    return Sharing.query.filter_by(sender_id=sender_id, receiver_id=receiver_id).first()

# 每 100g 平均热量
AVG_KCAL_TABLE = {
    "meat": 200,
    "vegetable": 35
}

def calculate_kcal_by_type(ingredient_type, grams):
    kcal_per_100g = AVG_KCAL_TABLE.get(ingredient_type.lower(), 0)
    return round((grams / 100.0) * kcal_per_100g, 2)


def process_ingredients(types, grams_choices, grams_customs):
    """
    Process ingredients and calculate totals.

    :param types: List of ingredient types.
    :param grams_choices: List of grams choices for each ingredient.
    :param grams_customs: List of custom grams for each ingredient.
    :return: A dictionary containing processed ingredients and totals.
    """
    ingredients = []
    total_kcal = 0
    veg_g = 0
    meat_g = 0

    for t, g_choice, g_custom in zip(types, grams_choices, grams_customs):
        grams = float(g_custom) if g_choice == "custom" and g_custom else float(g_choice)
        kcal = calculate_kcal_by_type(t, grams)
        total_kcal += kcal

        ingredients.append({
            "type": t,
            "grams": grams,
            "kcal": kcal
        })

        if t.lower() == "vegetable":
            veg_g += grams
        elif t.lower() == "meat":
            meat_g += grams

    total_g = veg_g + meat_g

    return {
        "ingredients": ingredients,
        "total_kcal": total_kcal,
        "veg_g": veg_g,
        "meat_g": meat_g,
        "total_g": total_g
    }


def save_recipe(user_id, title, date, servings, types, grams_choices, grams_customs):
    """
    Process ingredients and save the recipe to the database.

    :param title: Recipe title.
    :param servings: Number of servings.
    :param types: List of ingredient types.
    :param grams_choices: List of grams choices for each ingredient.
    :param grams_customs: List of custom grams for each ingredient.
    """
    # Process ingredients
    processed_data = process_ingredients(types, grams_choices, grams_customs)

    # Calculate kcal per serving
    total_kcal = processed_data["total_kcal"]
    kcal_per_serving = round(total_kcal / servings, 2)

    # Calculate total protein (25% of meat weight is protein)
    protein_g = round(processed_data["meat_g"] * 0.25, 2)

    # Save recipe to the database
    recipe = Recipe(
        name=title,
        user_id=user_id,
        created_at=date,
        servings=servings,
        total_kcal=round(total_kcal, 2),
        kcal_per_serving=kcal_per_serving,
        ingredients=json.dumps(processed_data["ingredients"]),
        veg_g=round(processed_data["veg_g"], 2),
        meat_g=round(processed_data["meat_g"], 2),
        total_g=round(processed_data["total_g"], 2),
        protein_g=protein_g
    )
    db.session.add(recipe)
    db.session.commit()


def get_last_7_days_recipes(user_id):
    """
    Fetch recipes created by the user in the last 7 days, sorted by creation date (ascending).

    :param user_id: The ID of the user.
    :return: A list of recipes created in the last 7 days by the user, sorted by date.
    """
    seven_days_ago = datetime.now() - timedelta(days=7)
    return Recipe.query.filter(
        Recipe.user_id == user_id,  # Filter by user_id
        Recipe.created_at >= seven_days_ago
    ).order_by(Recipe.created_at.asc()).all()  # Sort by created_at in ascending order


def daily_calories_one_serving(user_id):
    """
    Calculate daily calories (one serving) for the last 7 days.

    :param user_id: The ID of the user.
    :return: A list of dictionaries with date and calories per serving.
    """
    recipes = get_last_7_days_recipes(user_id)
    daily_calories = {}

    for recipe in recipes:
        date = recipe.created_at.strftime('%d %b')  # Format as '5 Aug'
        daily_calories[date] = daily_calories.get(date, 0) + recipe.kcal_per_serving

    return [{"date": date, "calories": round(calories, 2)} for date, calories in daily_calories.items()]

def proportion_of_veg_and_meat(user_id):
    """
    Calculate the proportion of vegetables and meat for the last 7 days.

    :param user_id: The ID of the user.
    :return: A dictionary with the proportion of vegetables and meat.
    """
    recipes = get_last_7_days_recipes(user_id)
    total_veg = 0
    total_meat = 0

    for recipe in recipes:
        total_veg += recipe.veg_g
        total_meat += recipe.meat_g

    total = total_veg + total_meat
    if total == 0:
        return {"vegetable": 0, "meat": 0}

    return {
        "vegetable": round((total_veg / total) * 100, 2),
        "meat": round((total_meat / total) * 100, 2)
    }


def daily_grams_of_food_one_serving(user_id):
    """
    Calculate the total grams of food (one serving) for each day in the last 7 days.

    :param user_id: The ID of the user.
    :return: A list of dictionaries with date and grams of food per serving.
    """
    recipes = get_last_7_days_recipes(user_id)
    daily_grams = {}

    for recipe in recipes:
        date = recipe.created_at.strftime('%d %b')  # Format as '5 Aug'
        grams_per_serving = recipe.total_g / recipe.servings
        daily_grams[date] = daily_grams.get(date, 0) + grams_per_serving

    return [{"date": date, "grams": round(grams, 2)} for date, grams in daily_grams.items()]


def daily_protein_one_serving(user_id):
    """
    Calculate daily protein (one serving) for the last 7 days.

    :param user_id: The ID of the user.
    :return: A list of dictionaries with date and protein per serving.
    """
    recipes = get_last_7_days_recipes(user_id)
    daily_protein = {}

    for recipe in recipes:
        date = recipe.created_at.strftime('%d %b')  # Format as '5 Aug'
        protein_per_serving = recipe.protein_g / recipe.servings
        daily_protein[date] = daily_protein.get(date, 0) + protein_per_serving

    return [{"date": date, "protein": round(protein, 2)} for date, protein in daily_protein.items()]


def get_sender_id_by_sharing_id(sharing_id):
    """
    Retrieve the sender's user ID based on the sharing ID.

    :param sharing_id: The ID of the sharing record.
    :return: The sender's user ID, or None if the sharing ID is invalid.
    """
    sharing = Sharing.query.filter_by(id=sharing_id).first()
    if sharing:
        return sharing.sender_id
    return None
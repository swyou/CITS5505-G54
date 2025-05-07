from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

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
# 每 100g 平均热量
AVG_KCAL_TABLE = {
    "meat": 200,
    "vegetable": 35
}

def calculate_kcal_by_type(ingredient_type, grams):
    kcal_per_100g = AVG_KCAL_TABLE.get(ingredient_type.lower(), 0)
    return round((grams / 100.0) * kcal_per_100g, 2)

@main.route('/upload', methods=['POST'])
def handle_upload():
    title = request.form.get("title")
    servings = int(request.form.get("servings") or 1)

    # 获取多个食材（数组）
    types = request.form.getlist("ingredient_type[]")
    grams_choices = request.form.getlist("ingredient_grams[]")
    grams_customs = request.form.getlist("ingredient_grams_custom[]")

    ingredients = []
    total_kcal = 0

    for t, g_choice, g_custom in zip(types, grams_choices, grams_customs):
        grams = float(g_custom) if g_choice == "custom" and g_custom else float(g_choice)
        kcal = calculate_kcal_by_type(t, grams)
        total_kcal += kcal
        ingredients.append({
            "type": t,
            "grams": grams,
            "kcal": kcal
        })

    kcal_per_serving = round(total_kcal / servings, 2)

    # ✅ 返回 JSON 数据
    return jsonify({
        "title": title,
        "servings": servings,
        "total_kcal": round(total_kcal, 2),
        "kcal_per_serving": kcal_per_serving,
        "ingredients": ingredients
    })

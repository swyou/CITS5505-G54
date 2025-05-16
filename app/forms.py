from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, FieldList, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Optional

# --------------------------
# Login Form
# --------------------------
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



# --------------------------
# Registration Form
# --------------------------
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')


# --------------------------
# Recipe Upload Form
# --------------------------
class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    servings = IntegerField('Servings', validators=[Optional()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    ingredient_type = FieldList(StringField('Ingredient Type'), min_entries=1)
    ingredient_name = FieldList(StringField('Ingredient Name'), min_entries=1)
    ingredient_grams = FieldList(StringField('Ingredient Grams'), min_entries=1)
    ingredient_grams_custom = FieldList(StringField('Ingredient Grams Custom'), min_entries=1)
    steps = StringField('Preparation Steps', validators=[Optional()])

    def validate(self, extra_validators=None):
        """
        Custom validation to ensure that for each ingredient,
        either predefined grams or a custom gram value is provided.
        """
        rv = super().validate(extra_validators=extra_validators)
        if not rv:
            return False

        # Ensure at least one of grams or grams_custom is filled for each ingredient
        for grams, grams_custom in zip(self.ingredient_grams.data, self.ingredient_grams_custom.data):
            if not grams and not grams_custom:
                self.ingredient_grams.errors.append(
                    "For each ingredient, either grams or custom grams must be provided."
                )
                return False
        return True



# --------------------------
# Share Data Form
# --------------------------
class ShareDataForm(FlaskForm):
    user = SelectField('Select a user', validators=[DataRequired()], coerce=int)
    # Dropdown list of available users to share data with (user IDs as values)
    submit = SubmitField('Share Data') # Submit button

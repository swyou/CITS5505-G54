import unittest
from app import create_app, db
from app.config import TestingConfig
from app.models import User, Recipe
from app.auth import creat_user
from datetime import datetime

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)  
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        """
        Test if a user is successfully created
        """
        user_name = "Test_user"
        creat_user(user_name, "UWA_secret")
        user = User.query.filter_by(username=user_name).first()
        self.assertIsNotNone(user)


    def test_user_duplication_check(self):
        """
        When a duplicated user name is given, test if the creation process is terminated.
        """
        user_name = "Duplicate_user"
        s1 = creat_user(user_name, "UWA_secret")
        s2 = creat_user(user_name, "UWA_secret")

        self.assertTrue(s1)
        self.assertFalse(s2)

    def test_login(self):
        user_name = "login_test"
        password = "login_password"
        creat_user(user_name, password)
        from app.auth import check_login

        user = check_login(user_name, password)
        self.assertIsNotNone(user)

    
    def test_process_ingredients(self):
        """
        Test the process_ingredients function to ensure it calculates the statistics of recipe correctly.
        """
        # Test data
        title = "Test Recipe"
        date = datetime.now()
        servings = 2
        types = ["meat", "vegetable"]
        grams_choices = ["100", "200"]
        grams_customs = ["", ""]

        # create one user to ensure there is at least one user
        creat_user("test_process_ingredients", "UWA_secret")
        user = User.query.filter_by(username="test_process_ingredients").first()
        user_id = user.id

        from app.service import process_ingredients
        result = process_ingredients(types, grams_choices, grams_customs)

        # Assertions
        self.assertEqual(len(result["ingredients"]), 2)
        self.assertEqual(result["total_kcal"], 270.0)
        self.assertEqual(result["veg_g"], 200.0)
        self.assertEqual(result["meat_g"], 100.0)
        self.assertEqual(result["total_g"], 300.0)
        self.assertIn("type", result["ingredients"][0])
        self.assertIn("grams", result["ingredients"][0])
        self.assertIn("kcal", result["ingredients"][0])


    def test_save_recipe(self):
        """
        Test the save_recipe function to ensure it saves the recipe correctly.
        """
        # Test data
        user_id = 1
        title = "Test Recipe"
        date = datetime.now()
        servings = 2
        types = ["meat", "vegetable"]
        grams_choices = ["100", "200"]
        grams_customs = ["", ""]

        from app.service import save_recipe
        save_recipe(user_id, title, date, servings, types, grams_choices, grams_customs)

        recipe = Recipe.query.filter_by(user_id=user_id, name=title).first()

        self.assertIsNotNone(recipe)
        self.assertEqual(recipe.name, title)
        self.assertEqual(recipe.user_id, user_id)
        self.assertEqual(recipe.servings, servings)
        self.assertEqual(recipe.total_kcal, 270.0)
        self.assertEqual(recipe.kcal_per_serving, 135.0)
        self.assertEqual(recipe.veg_g, 200.0)
        self.assertEqual(recipe.meat_g, 100.0)
        self.assertEqual(recipe.total_g, 300.0)
        self.assertEqual(recipe.protein_g, 25.0)


    def test_share_functionality(self):
        from app.service import create_sharing
        from app.models import Sharing

        # create two user to ensure there is at least two users
        creat_user("test_share_functionality1", "UWA_secret")
        creat_user("test_share_functionality2", "UWA_secret")
        user1 = User.query.filter_by(username="test_share_functionality1").first()
        user2 = User.query.filter_by(username="test_share_functionality2").first()

        create_sharing(user1.id, user2.id, "share")

        sharing = Sharing.query.filter_by(sender_id=user1.id, receiver_id=user2.id).first()

        self.assertIsNotNone(sharing)
        

if __name__ == '__main__':
    unittest.main()



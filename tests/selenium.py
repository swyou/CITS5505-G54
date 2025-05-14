import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from threading import Thread
from app import create_app
from app.config import TestingConfig
from app import db


_TEST_USER_1 = "test_user1"
_TEST_USER_1_PW = "fusioufisonihi1"

_TEST_USER_2 = "test_user2"
_TEST_USER_2_PW = "fusioufisonihi2"

class TestSelenium(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the Flask server in a separate thread
        cls.app = create_app(TestingConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        # create test user
        from app.auth import creat_user
        creat_user(_TEST_USER_1, _TEST_USER_1_PW)
        creat_user(_TEST_USER_2, _TEST_USER_2_PW)

        cls.server_thread = Thread(target=cls.app.run)
        cls.server_thread.setDaemon(True)
        cls.server_thread.start()
        
        options = Options()
        options.add_argument("--disable-features=PasswordCheck")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        options.add_experimental_option("prefs", prefs)

        cls.driver = webdriver.Chrome(options=options)
        cls.base_url = "http://127.0.0.1:5000"

    @classmethod
    def tearDownClass(cls):
        # Quit the WebDriver
        cls.driver.quit()

        # Clean up the database
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

        # Stop the Flask server
        cls.server_thread.join(timeout=1)


    def test_login_success(self):
        """Test successful login."""
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.NAME, "username").send_keys(_TEST_USER_1)
        self.driver.find_element(By.NAME, "password").send_keys(_TEST_USER_1_PW)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait for redirection and check if the user is logged in
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main-content"))
        )
        self.assertIn("SmartBite", self.driver.title)
        # make sure logged out 
        self.logout()

    def test_login_failure(self):
        """Test login failure with incorrect credentials."""
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.NAME, "username").send_keys(_TEST_USER_1)
        self.driver.find_element(By.NAME, "password").send_keys("jfosiufisoufisdufio")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait for the flash message to appear
        flash_message = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "custom-flash"))
        )
        self.assertIn("danger", flash_message.get_attribute("class"))
        self.assertIn("Invalid", flash_message.text)


    def test_fill_recipe_form_success(self):

        self.login()

        """Test filling and submitting the recipe upload form successfully."""
        self.driver.get(f"{self.base_url}/upload")

        # Fill in the dish name
        self.driver.find_element(By.NAME, "title").send_keys("Test Dish")

        # Add an ingredient
        # self.driver.find_element(By.CSS_SELECTOR, ".btn-outline").click()

        self.driver.find_element(By.NAME, "ingredient_name-0").send_keys("Carrot")
        select_element = self.driver.find_element(By.NAME, "ingredient_grams-0")
        # Select 100g
        select = Select(select_element)
        select.select_by_index(1) 
        # Fill in preparation steps
        self.driver.find_element(By.NAME, "steps").send_keys("Chop and cook.")

        # Fill in servings
        self.driver.find_element(By.NAME, "servings").send_keys("2")

        # Submit the form
        self.driver.find_element(By.ID, "submit-recipe").send_keys(Keys.ENTER)

        # Wait for success alert or redirection
        WebDriverWait(self.driver, 5).until(
            EC.alert_is_present()  # Assuming an alert is shown on success
        )
        alert = self.driver.switch_to.alert
        print(alert.text)
        self.assertIn("Recipe submitted successfully", alert.text)

        alert.accept()
        self.logout()


    def test_register_success(self):
        """Test successful registration."""
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "showRegister").click()


        self.driver.execute_script("""
            document.querySelector('#registerForm [name="username"]').value = 'test_user3';
            document.querySelector('#registerForm [name="password"]').value = 'fusioufisonihi2';
            document.querySelector('#registerForm [name="confirm_password"]').value = 'fusioufisonihi2';
        """)

        self.driver.execute_script("document.querySelector('#registerForm button[type=\"submit\"]').click();")

        # Wait for success flash message
        flash_message = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "custom-flash"))
        )
        self.assertIn("success", flash_message.get_attribute("class"))
        self.assertIn("Registration successful", flash_message.text)

    def test_register_failure(self):
        """Test registration failure with mismatched passwords."""
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "showRegister").click()

        # Fill in the registration form with mismatched passwords
        self.driver.execute_script("""
            document.querySelector('#registerForm [name="username"]').value = 'test_user3';
            document.querySelector('#registerForm [name="password"]').value = 'fusioufisonihi2';
            document.querySelector('#registerForm [name="confirm_password"]').value = 'fusioufisonihi1';
        """)
        self.driver.execute_script("document.querySelector('#registerForm button[type=\"submit\"]').click();")

        # Wait for failure flash message
        flash_message = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "custom-flash"))
        )

        self.assertIn("danger", flash_message.get_attribute("class"))
        self.assertIn("Passwords do not match", flash_message.text)

    def test_share_data(self):
        self.login()
        """Test sharing data with another user."""
        self.driver.get(f"{self.base_url}/share")

        # Wait for the user dropdown to load
        user_dropdown = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "userDropdown"))
        )

        # Select a user from the dropdown
        user_dropdown.click()
        user_option = self.driver.find_element(By.XPATH, "//option[not(@disabled)]")  # Select the first enabled option
        user_option.click()

        # Click the Share Data button
        share_button = self.driver.find_element(By.ID, "shareButton")
        share_button.click()

        # Wait for the alert and verify the message
        WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert_text = alert.text

        # Check if the alert indicates success or already shared
        self.assertTrue(
            "Data shared successfully!" in alert_text or "You have already shared data with this user." in alert_text
        )
        alert.accept()
        self.logout()


    def login(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.execute_script("""
            document.querySelector('[name="username"]').value = arguments[0];
            document.querySelector('[name="password"]').value = arguments[1];
        """, _TEST_USER_1, _TEST_USER_1_PW)

        # 提交表单
        self.driver.execute_script("document.querySelector('button[type=\"submit\"]').click();")

        # 等待页面加载完成
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main-content"))
        )

    def logout(self):
        self.driver.find_element(By.ID, "logout_btn").click()
        WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()


if __name__ == "__main__":
    unittest.main()
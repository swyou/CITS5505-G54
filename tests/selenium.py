import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.safari.service import Service

class TestSelenium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the Selenium WebDriver with SafariDriver
        cls.driver = webdriver.Safari(service=Service())
        cls.base_url = "http://127.0.0.1:5500"  

    @classmethod
    def tearDownClass(cls):
        # Quit the WebDriver after all tests
        cls.driver.quit()

    def test_login_success(self):
        """Test successful login."""
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.NAME, "username").send_keys("testuser")
        self.driver.find_element(By.NAME, "password").send_keys("testpassword")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait for redirection and check if the user is logged in
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main-content"))
        )
        self.assertIn("SmartBite", self.driver.title)

    def test_login_failure(self):
        """Test login failure with incorrect credentials."""
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.NAME, "username").send_keys("wronguser")
        self.driver.find_element(By.NAME, "password").send_keys("wrongpassword")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait for the flash message to appear
        flash_message = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "custom-flash"))
        )
        self.assertIn("danger", flash_message.get_attribute("class"))
        self.assertIn("Invalid", flash_message.text)

    def test_fill_recipe_form_success(self):
        """Test filling and submitting the recipe upload form successfully."""
        self.driver.get(f"{self.base_url}/upload")

        # Fill in the dish name
        self.driver.find_element(By.NAME, "title").send_keys("Test Dish")

        # Add an ingredient
        self.driver.find_element(By.CSS_SELECTOR, ".btn-outline").click()
        ingredient_name = self.driver.find_elements(By.NAME, "ingredient_name[]")[-1]
        ingredient_name.send_keys("Carrot")
        ingredient_grams = self.driver.find_elements(By.NAME, "ingredient_grams[]")[-1]
        ingredient_grams.send_keys(Keys.DOWN, Keys.ENTER)  # Select 100g

        # Fill in preparation steps
        self.driver.find_element(By.NAME, "steps").send_keys("Chop and cook.")

        # Fill in servings
        self.driver.find_element(By.NAME, "servings").send_keys("2")

        # Fill in the date
        date_input = self.driver.find_element(By.NAME, "date")
        date_input.clear()
        date_input.send_keys("2023-10-01")

        # Submit the form
        self.driver.find_element(By.CSS_SELECTOR, ".btn-orange").click()

        # Wait for success alert or redirection
        WebDriverWait(self.driver, 5).until(
            EC.alert_is_present()  # Assuming an alert is shown on success
        )
        alert = self.driver.switch_to.alert
        self.assertIn("Recipe submitted successfully", alert.text)
        alert.accept()

    def test_fill_recipe_form_failure(self):
        """Test recipe form submission failure with missing required fields."""
        self.driver.get(f"{self.base_url}/upload")

        # Leave the dish name empty
        self.driver.find_element(By.NAME, "title").send_keys("")

        # Submit the form
        self.driver.find_element(By.CSS_SELECTOR, ".btn-orange").click()

        # Wait for the flash message or validation error
        flash_message = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "custom-flash"))
        )
        self.assertIn("danger", flash_message.get_attribute("class"))
        self.assertIn("Please fill out this field", flash_message.text)

    def test_register_success(self):
        """Test successful registration."""
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "showRegister").click()

        # Fill in the registration form
        self.driver.find_element(By.NAME, "username").send_keys("newuser")
        self.driver.find_element(By.NAME, "password").send_keys("newpassword")
        self.driver.find_element(By.NAME, "confirm_password").send_keys("newpassword")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

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
        self.driver.find_element(By.NAME, "username").send_keys("newuser")
        self.driver.find_element(By.NAME, "password").send_keys("password1")
        self.driver.find_element(By.NAME, "confirm_password").send_keys("password2")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait for failure flash message
        flash_message = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "custom-flash"))
        )
        self.assertIn("danger", flash_message.get_attribute("class"))
        self.assertIn("Passwords do not match", flash_message.text)

    def test_share_data(self):
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

    def test_nutrition_trends(self):
        """Test if the chart changes when selecting 'Myself' and another user in the dropdown."""
        self.driver.get(f"{self.base_url}/data")

        # Wait for the page to load and the default chart to appear
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "caloriesChart"))
        )
        self.assertTrue(self.driver.find_element(By.ID, "caloriesChart").is_displayed())

        # Get the initial chart content for "Myself"
        chart_canvas = self.driver.find_element(By.ID, "caloriesChart")
        initial_chart_content = chart_canvas.get_attribute("data-chart-content")  # Hypothetical attribute

        # Select another user from the dropdown
        shared_reports_dropdown = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "sharedReports"))
        )
        shared_reports_dropdown.click()
        other_user_option = self.driver.find_element(By.XPATH, "//option[not(@disabled) and @value!='myself']")
        other_user_option.click()

        # Wait for the chart to update
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "caloriesChart"))
        )

        # Get the updated chart content for the other user
        updated_chart_content = chart_canvas.get_attribute("data-chart-content")  # Hypothetical attribute

        # Verify that the chart content is different
        self.assertNotEqual(initial_chart_content, updated_chart_content, "The chart content should differ between 'Myself' and another user.")

if __name__ == "__main__":
    unittest.main()
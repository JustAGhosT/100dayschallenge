#!/usr/bin/env python3
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import json

# Get the frontend URL from frontend/.env
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
print(f"Testing frontend at: {FRONTEND_URL}")

# Test user credentials
TEST_USER_EMAIL = "test.user@example.com"
TEST_USER_PASSWORD = "test-password-123"  # In a real scenario, use environment variables

class FrontendTests(unittest.TestCase):
    """Test suite for Challenge Tracker Platform frontend UI"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment once before all tests"""
        # Initialize WebDriver (Chrome in headless mode)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.set_window_size(1920, 1080)
        cls.wait = WebDriverWait(cls.driver, 10)
        print("✅ Initialized WebDriver for UI testing")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        cls.driver.quit()
        print("✅ Closed WebDriver")
    
    def test_01_landing_page(self):
        """Test the landing page loads correctly"""
        self.driver.get(FRONTEND_URL)
        
        # Check title
        self.assertIn("Challenge Tracker", self.driver.title)
        
        # Check main elements
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            header = self.driver.find_element(By.TAG_NAME, "h1")
            self.assertIn("Challenge", header.text)
            
            # Check for login/signup buttons
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
            self.assertTrue(login_button.is_displayed())
            
            # Check for feature sections
            features = self.driver.find_elements(By.CLASS_NAME, "feature-card")
            self.assertGreaterEqual(len(features), 3)
            
            print("✅ Landing page loads correctly")
        except TimeoutException:
            self.fail("Landing page did not load properly")
    
    def test_02_login_flow(self):
        """Test the login functionality"""
        self.driver.get(FRONTEND_URL)
        
        try:
            # Click login button
            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
            login_button.click()
            
            # Wait for login modal/page
            email_input = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
            password_input = self.driver.find_element(By.ID, "password")
            
            # Enter credentials
            email_input.send_keys(TEST_USER_EMAIL)
            password_input.send_keys(TEST_USER_PASSWORD)
            
            # Submit form
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            # Wait for dashboard to load after login
            self.wait.until(EC.url_contains("/dashboard"))
            
            # Verify we're on the dashboard
            self.assertIn("/dashboard", self.driver.current_url)
            
            # Store cookies for subsequent tests
            FrontendTests.cookies = self.driver.get_cookies()
            
            print("✅ Login flow works correctly")
        except TimeoutException:
            self.fail("Login flow failed")
    
    def test_03_dashboard_elements(self):
        """Test the dashboard UI elements"""
        # Make sure we're logged in
        self._ensure_logged_in()
        
        try:
            # Check for user info
            user_name = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "user-name")))
            self.assertTrue(user_name.is_displayed())
            
            # Check for stats cards
            stat_cards = self.driver.find_elements(By.CLASS_NAME, "stat-card")
            self.assertGreaterEqual(len(stat_cards), 3)
            
            # Check for recent challenges section
            challenges_section = self.driver.find_element(By.XPATH, "//h2[contains(text(), 'Challenges')]")
            self.assertTrue(challenges_section.is_displayed())
            
            # Check for create challenge button
            create_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Create')]")
            self.assertTrue(create_button.is_displayed())
            
            print("✅ Dashboard UI elements display correctly")
        except TimeoutException:
            self.fail("Dashboard elements not found")
    
    def test_04_create_challenge_flow(self):
        """Test creating a new challenge"""
        # Make sure we're logged in
        self._ensure_logged_in()
        
        try:
            # Navigate to challenges page
            challenges_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/challenges')]")))
            challenges_link.click()
            
            # Wait for challenges page to load
            self.wait.until(EC.url_contains("/challenges"))
            
            # Click create challenge button
            create_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create')]")))
            create_button.click()
            
            # Wait for challenge form
            title_input = self.wait.until(EC.presence_of_element_located((By.ID, "title")))
            
            # Fill out form
            challenge_title = f"Test Challenge {int(time.time())}"
            title_input.send_keys(challenge_title)
            
            description_input = self.driver.find_element(By.ID, "description")
            description_input.send_keys("This is a test challenge created by automated tests")
            
            duration_input = self.driver.find_element(By.ID, "duration_days")
            duration_input.clear()
            duration_input.send_keys("30")
            
            # Add a goal
            goal_input = self.driver.find_element(By.ID, "goal")
            goal_input.send_keys("Complete all test cases")
            add_goal_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Add Goal')]")
            add_goal_button.click()
            
            # Add a rule
            rule_input = self.driver.find_element(By.ID, "rule")
            rule_input.send_keys("Write tests first")
            add_rule_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Add Rule')]")
            add_rule_button.click()
            
            # Submit form
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            # Wait for redirect to challenge detail page
            self.wait.until(EC.url_contains("/challenges/"))
            
            # Verify challenge was created
            page_title = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            self.assertEqual(challenge_title, page_title.text)
            
            # Store challenge URL for subsequent tests
            FrontendTests.challenge_url = self.driver.current_url
            
            print(f"✅ Challenge creation flow works correctly, created: {challenge_title}")
        except TimeoutException as e:
            self.fail(f"Challenge creation flow failed: {str(e)}")
    
    def test_05_create_project_flow(self):
        """Test creating a new project within a challenge"""
        # Make sure we're logged in and on the challenge page
        self._ensure_logged_in()
        self.driver.get(FrontendTests.challenge_url)
        
        try:
            # Click add project button
            add_project_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Project')]")))
            add_project_button.click()
            
            # Wait for project form
            title_input = self.wait.until(EC.presence_of_element_located((By.ID, "title")))
            
            # Fill out form
            project_title = f"Test Project {int(time.time())}"
            title_input.send_keys(project_title)
            
            description_input = self.driver.find_element(By.ID, "description")
            description_input.send_keys("This is a test project created by automated tests")
            
            repo_input = self.driver.find_element(By.ID, "repository_url")
            repo_input.send_keys("https://github.com/testuser/test-project")
            
            demo_input = self.driver.find_element(By.ID, "demo_url")
            demo_input.send_keys("https://test-project.example.com")
            
            # Add tech stack
            tech_input = self.driver.find_element(By.ID, "tech")
            tech_input.send_keys("Python")
            add_tech_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Add Tech')]")
            add_tech_button.click()
            
            tech_input.clear()
            tech_input.send_keys("React")
            add_tech_button.click()
            
            # Submit form
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            # Wait for redirect back to challenge detail page
            self.wait.until(EC.url_contains(FrontendTests.challenge_url))
            
            # Verify project was added to the list
            project_cards = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "project-card")))
            self.assertGreaterEqual(len(project_cards), 1)
            
            project_titles = [card.find_element(By.TAG_NAME, "h3").text for card in project_cards]
            self.assertIn(project_title, project_titles)
            
            print(f"✅ Project creation flow works correctly, created: {project_title}")
        except TimeoutException:
            self.fail("Project creation flow failed")
    
    def test_06_project_detail_view(self):
        """Test viewing project details"""
        # Make sure we're logged in and on the challenge page
        self._ensure_logged_in()
        self.driver.get(FrontendTests.challenge_url)
        
        try:
            # Find and click on the first project card
            project_card = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "project-card")))
            project_card.click()
            
            # Wait for project detail page
            self.wait.until(EC.url_contains("/projects/"))
            
            # Check project details are displayed
            title = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            self.assertTrue(title.is_displayed())
            
            description = self.driver.find_element(By.CLASS_NAME, "project-description")
            self.assertTrue(description.is_displayed())
            
            # Check for tech stack tags
            tech_tags = self.driver.find_elements(By.CLASS_NAME, "tech-tag")
            self.assertGreaterEqual(len(tech_tags), 1)
            
            # Check for repository and demo links
            repo_link = self.driver.find_element(By.XPATH, "//a[contains(@href, 'github.com')]")
            self.assertTrue(repo_link.is_displayed())
            
            print("✅ Project detail view works correctly")
        except TimeoutException:
            self.fail("Project detail view failed to load")
    
    def test_07_logout_flow(self):
        """Test the logout functionality"""
        # Make sure we're logged in
        self._ensure_logged_in()
        
        try:
            # Click user menu
            user_menu = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "user-menu")))
            user_menu.click()
            
            # Click logout
            logout_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Logout')]")))
            logout_button.click()
            
            # Wait for redirect to landing page
            self.wait.until(EC.url_to_be(FRONTEND_URL))
            
            # Verify login button is visible again
            login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Login')]")))
            self.assertTrue(login_button.is_displayed())
            
            print("✅ Logout flow works correctly")
        except TimeoutException:
            self.fail("Logout flow failed")
    
    def _ensure_logged_in(self):
        """Helper method to ensure we're logged in for tests that require authentication"""
        # Check if we're already on a page that requires auth
        if "/dashboard" in self.driver.current_url or "/challenges" in self.driver.current_url:
            return
        
        # If we have cookies from a previous login, use them
        if hasattr(FrontendTests, 'cookies'):
            self.driver.get(FRONTEND_URL)
            for cookie in FrontendTests.cookies:
                self.driver.add_cookie(cookie)
            self.driver.get(f"{FRONTEND_URL}/dashboard")
            try:
                # Wait for dashboard to confirm we're logged in
                self.wait.until(EC.url_contains("/dashboard"))
                return
            except TimeoutException:
                pass  # Cookie login failed, continue to manual login
        
        # Manual login
        self.test_02_login_flow()


if __name__ == "__main__":
    # Run the tests in order
    unittest.main(verbosity=2)
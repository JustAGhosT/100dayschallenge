#!/usr/bin/env python3
import unittest
import requests
import json
import time
import os
import pymongo
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta

# Get environment variables
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:5000')
API_URL = f"{BACKEND_URL}/api"

# MongoDB connection info
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'test_database')

# Connect to MongoDB directly for test setup
mongo_client = pymongo.MongoClient(MONGO_URL)
db = mongo_client[DB_NAME]

# Test data
TEST_USER = {
    "id": str(uuid.uuid4()),
    "email": "integration.test@example.com",
    "name": "Integration Test User",
    "picture": "https://example.com/profile.jpg",
    "created_at": datetime.utcnow()
}

TEST_SESSION = {
    "id": str(uuid.uuid4()),
    "user_id": TEST_USER["id"],
    "session_token": f"test-token-{uuid.uuid4()}",
    "expires_at": datetime.utcnow() + timedelta(days=7),
    "created_at": datetime.utcnow()
}

class IntegrationTests(unittest.TestCase):
    """Integration tests for Challenge Tracker Platform"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment once before all tests"""
        # Create test user and session in database
        db.users.delete_many({"email": TEST_USER["email"]})
        db.users.insert_one(TEST_USER)
        db.sessions.insert_one(TEST_SESSION)
        
        # Store auth token for API tests
        cls.auth_token = TEST_SESSION["session_token"]
        cls.user_id = TEST_USER["id"]
        
        # Initialize WebDriver for UI tests
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.set_window_size(1920, 1080)
        cls.wait = WebDriverWait(cls.driver, 10)
        
        print(f"✅ Set up integration test environment")
        print(f"   - Frontend URL: {FRONTEND_URL}")
        print(f"   - Backend API URL: {API_URL}")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        # Clean up test data
        db.users.delete_many({"id": cls.user_id})
        db.sessions.delete_many({"user_id": cls.user_id})
        db.challenges.delete_many({"user_id": cls.user_id})
        db.projects.delete_many({"user_id": cls.user_id})
        
        # Close WebDriver
        cls.driver.quit()
        
        print(f"✅ Cleaned up integration test environment")
    
    def test_01_api_create_and_ui_verify_challenge(self):
        """Create a challenge via API and verify it appears in the UI"""
        # 1. Create challenge via API
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        challenge_data = {
            "title": "Integration Test Challenge",
            "description": "Testing API and UI integration",
            "goals": ["Verify API creates data", "Verify UI displays data"],
            "rules": ["Test must pass end-to-end", "No mocking allowed"],
            "duration_days": 14
        }
        
        response = requests.post(
            f"{API_URL}/challenges", 
            headers=headers,
            json=challenge_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        challenge_id = data["id"]
        
        # 2. Login to UI and navigate to challenges
        self._login_to_ui()
        self.driver.get(f"{FRONTEND_URL}/challenges")
        
        # 3. Verify the challenge appears in the UI
        try:
            # Wait for challenges to load
            challenge_cards = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "challenge-card")))
            
            # Find our challenge by title
            found = False
            for card in challenge_cards:
                title_element = card.find_element(By.TAG_NAME, "h3")
                if challenge_data["title"] in title_element.text:
                    found = True
                    break
            
            self.assertTrue(found, "Challenge created via API was not found in UI")
            
            # Store challenge ID for subsequent tests
            IntegrationTests.challenge_id = challenge_id
            
            print("✅ Challenge created via API appears correctly in UI")
        except TimeoutException:
            self.fail("Challenge list did not load in UI")
    
    def test_02_ui_create_and_api_verify_project(self):
        """Create a project via UI and verify it via API"""
        # 1. Login and navigate to the challenge detail page
        self._login_to_ui()
        self.driver.get(f"{FRONTEND_URL}/challenges/{IntegrationTests.challenge_id}")
        
        # 2. Create a project via UI
        try:
            # Click add project button
            add_project_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Project')]")))
            add_project_button.click()
            
            # Wait for project form
            title_input = self.wait.until(EC.presence_of_element_located((By.ID, "title")))
            
            # Fill out form
            project_title = f"Integration Test Project {int(time.time())}"
            title_input.send_keys(project_title)
            
            description_input = self.driver.find_element(By.ID, "description")
            description_input.send_keys("This project tests UI to API integration")
            
            repo_input = self.driver.find_element(By.ID, "repository_url")
            repo_input.send_keys("https://github.com/testuser/integration-test")
            
            # Submit form
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            # Wait for redirect back to challenge detail page
            self.wait.until(EC.url_contains(f"/challenges/{IntegrationTests.challenge_id}"))
            
            # Store project title for API verification
            IntegrationTests.project_title = project_title
            
        except TimeoutException:
            self.fail("Failed to create project via UI")
        
        # 3. Verify the project via API
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = requests.get(
            f"{API_URL}/challenges/{IntegrationTests.challenge_id}/projects", 
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        projects = response.json()
        
        # Find our project by title
        found = False
        for project in projects:
            if project["title"] == IntegrationTests.project_title:
                found = True
                IntegrationTests.project_id = project["id"]
                break
        
        self.assertTrue(found, "Project created via UI was not found via API")
        print("✅ Project created via UI is correctly stored in the database and accessible via API")
    
    def test_03_api_update_and_ui_verify_project(self):
        """Update a project via API and verify changes in UI"""
        # 1. Update project via API
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        update_data = {
            "title": f"Updated {IntegrationTests.project_title}",
            "description": "This project was updated via API",
            "status": "completed",
            "progress_percentage": 100
        }
        
        response = requests.put(
            f"{API_URL}/projects/{IntegrationTests.project_id}", 
            headers=headers,
            json=update_data
        )
        
        self.assertEqual(response.status_code, 200)
        
        # 2. Verify changes in UI
        self._login_to_ui()
        self.driver.get(f"{FRONTEND_URL}/challenges/{IntegrationTests.challenge_id}")
        
        try:
            # Wait for projects to load
            project_cards = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "project-card")))
            
            # Find our updated project by title
            found = False
            for card in project_cards:
                title_element = card.find_element(By.TAG_NAME, "h3")
                if update_data["title"] in title_element.text:
                    found = True
                    
                    # Verify status is displayed as completed
                    status_element = card.find_element(By.CLASS_NAME, "status-badge")
                    self.assertIn("completed", status_element.text.lower())
                    
                    # Verify progress percentage
                    progress_element = card.find_element(By.CLASS_NAME, "progress-indicator")
                    self.assertIn("100", progress_element.text)
                    
                    break
            
            self.assertTrue(found, "Updated project was not found in UI")
            print("✅ Project updated via API shows correct changes in UI")
        except TimeoutException:
            self.fail("Project list did not load in UI")
    
    def test_04_ui_delete_and_api_verify_project(self):
        """Delete a project via UI and verify deletion via API"""
        # 1. Login and navigate to the project detail page
        self._login_to_ui()
        self.driver.get(f"{FRONTEND_URL}/projects/{IntegrationTests.project_id}")
        
        try:
            # Click delete button
            delete_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Delete')]")))
            delete_button.click()
            
            # Confirm deletion in modal
            confirm_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]")))
            confirm_button.click()
            
            # Wait for redirect back to challenge detail page
            self.wait.until(EC.url_contains(f"/challenges/{IntegrationTests.challenge_id}"))
            
        except TimeoutException:
            self.fail("Failed to delete project via UI")
        
        # 2. Verify deletion via API
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = requests.get(
            f"{API_URL}/projects/{IntegrationTests.project_id}", 
            headers=headers
        )
        
        self.assertEqual(response.status_code, 404, "Project should return 404 after deletion")
        print("✅ Project deleted via UI is correctly removed from the database")
    
    def test_05_real_time_updates(self):
        """Test real-time updates between multiple clients"""
        # This test simulates two clients by using both API and UI
        
        # 1. Create a new challenge via API
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        challenge_data = {
            "title": "Real-time Test Challenge",
            "description": "Testing real-time updates between clients",
            "duration_days": 7
        }
        
        response = requests.post(
            f"{API_URL}/challenges", 
            headers=headers,
            json=challenge_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        realtime_challenge_id = data["id"]
        
        # 2. Open the UI to the challenges list page
        self._login_to_ui()
        self.driver.get(f"{FRONTEND_URL}/challenges")
        
        # Wait for challenges to load
        challenge_cards = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "challenge-card")))
        initial_count = len(challenge_cards)
        
        # 3. Create another challenge via API while UI is open
        new_challenge_data = {
            "title": "Second Real-time Test Challenge",
            "description": "This should appear in UI without refresh",
            "duration_days": 7
        }
        
        response = requests.post(
            f"{API_URL}/challenges", 
            headers=headers,
            json=new_challenge_data
        )
        
        self.assertEqual(response.status_code, 200)
        
        # 4. Wait for real-time update in UI (without refreshing)
        try:
            # Wait for the challenge count to increase
            def challenge_count_increased(driver):
                cards = driver.find_elements(By.CLASS_NAME, "challenge-card")
                return len(cards) > initial_count
            
            self.wait.until(challenge_count_increased)
            
            # Verify the new challenge appears
            updated_cards = self.driver.find_elements(By.CLASS_NAME, "challenge-card")
            
            # Find our new challenge by title
            found = False
            for card in updated_cards:
                title_element = card.find_element(By.TAG_NAME, "h3")
                if new_challenge_data["title"] in title_element.text:
                    found = True
                    break
            
            self.assertTrue(found, "New challenge created via API did not appear in UI via real-time update")
            print("✅ Real-time updates work correctly between API and UI")
        except TimeoutException:
            self.fail("Real-time update did not occur in UI")
    
    def _login_to_ui(self):
        """Helper method to login to the UI using test session"""
        # Navigate to frontend
        self.driver.get(FRONTEND_URL)
        
        # Inject session token via localStorage
        script = f"""
        localStorage.setItem('auth_token', '{self.auth_token}');
        localStorage.setItem('user_id', '{self.user_id}');
        localStorage.setItem('user_email', '{TEST_USER["email"]}');
        localStorage.setItem('user_name', '{TEST_USER["name"]}');
        """
        self.driver.execute_script(script)
        
        # Navigate to dashboard to activate the session
        self.driver.get(f"{FRONTEND_URL}/dashboard")
        
        # Wait for dashboard to load
        try:
            self.wait.until(EC.url_contains("/dashboard"))
            return True
        except TimeoutException:
            return False


if __name__ == "__main__":
    # Run the tests in order
    unittest.main(verbosity=2)
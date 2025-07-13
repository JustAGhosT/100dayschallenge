#!/usr/bin/env python3
"""
End-to-End Test for Challenge Creation and Management Flow

This script tests the complete flow of creating and managing challenges.
"""

import os
import sys
import unittest
import time
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test automation utilities
from automation.test_automation_setup import (
    setup_test_environment,
    setup_ui_helper,
    setup_api_helper
)

class TestChallengeFlow(unittest.TestCase):
    """Test the challenge creation and management flow."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the test environment once before all tests."""
        cls.env = setup_test_environment()
        cls.api_helper = setup_api_helper(cls.env)
        
        # Log in via API to get authentication token
        cls.user_data = cls.api_helper.login()
        
        # Set up UI helper with Chrome browser
        cls.ui_helper = setup_ui_helper("chrome", True, cls.env)
        
        print(f"✅ Test environment set up")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        # Close the browser
        if hasattr(cls, 'ui_helper') and cls.ui_helper.driver:
            cls.ui_helper.driver.quit()
        
        print(f"✅ Test environment cleaned up")
    
    def setUp(self):
        """Set up before each test."""
        # Navigate to home page and ensure we're logged in
        self.ui_helper.navigate_to("/")
        
        # Check if we need to log in
        if "/login" in self.ui_helper.driver.current_url or "Login" in self.ui_helper.driver.page_source:
            self.ui_helper.login()
        
        print(f"✅ Test setup complete")
    
    def test_01_create_challenge(self):
        """Test creating a new challenge."""
        # Generate unique challenge title
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        challenge_title = f"Test Challenge {timestamp}"
        challenge_description = "This is an automated test challenge"
        
        # Navigate to challenges page
        self.ui_helper.navigate_to("/challenges")
        
        # Create a new challenge
        self.ui_helper.create_challenge(
            title=challenge_title,
            description=challenge_description,
            duration=30
        )
        
        # Verify we're on the challenge detail page
        self.assertTrue("/challenges/" in self.ui_helper.driver.current_url)
        
        # Verify challenge title is displayed
        page_title = self.ui_helper.wait_for_element(By.TAG_NAME, "h1").text
        self.assertEqual(challenge_title, page_title)
        
        # Store challenge URL for subsequent tests
        self.__class__.challenge_url = self.ui_helper.driver.current_url
        
        print(f"✅ Challenge created: {challenge_title}")
    
    def test_02_add_project_to_challenge(self):
        """Test adding a project to a challenge."""
        # Navigate to the challenge created in the previous test
        self.ui_helper.driver.get(self.__class__.challenge_url)
        
        # Generate unique project title
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        project_title = f"Test Project {timestamp}"
        project_description = "This is an automated test project"
        
        # Create a new project
        self.ui_helper.create_project(
            title=project_title,
            description=project_description,
            repository_url="https://github.com/testuser/test-project",
            demo_url="https://example.com/demo"
        )
        
        # Verify project is added to the challenge
        project_elements = self.ui_helper.driver.find_elements(By.CLASS_NAME, "project-card")
        self.assertGreaterEqual(len(project_elements), 1)
        
        # Verify project title is displayed
        project_titles = [el.find_element(By.TAG_NAME, "h3").text for el in project_elements]
        self.assertIn(project_title, project_titles)
        
        print(f"✅ Project added: {project_title}")
    
    def test_03_update_challenge(self):
        """Test updating a challenge."""
        # Navigate to the challenge created in the previous test
        self.ui_helper.driver.get(self.__class__.challenge_url)
        
        # Click edit button
        edit_button = self.ui_helper.wait_for_clickable(By.XPATH, "//button[contains(text(), 'Edit')]")
        edit_button.click()
        
        # Update challenge title
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        updated_title = f"Updated Challenge {timestamp}"
        
        title_input = self.ui_helper.wait_for_element(By.ID, "title")
        title_input.clear()
        title_input.send_keys(updated_title)
        
        # Submit form
        submit_button = self.ui_helper.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
        
        # Wait for update to complete
        time.sleep(1)
        
        # Verify challenge title is updated
        page_title = self.ui_helper.wait_for_element(By.TAG_NAME, "h1").text
        self.assertEqual(updated_title, page_title)
        
        print(f"✅ Challenge updated: {updated_title}")
    
    def test_04_update_project_status(self):
        """Test updating a project's status."""
        # Navigate to the challenge
        self.ui_helper.driver.get(self.__class__.challenge_url)
        
        # Click on the first project
        project_card = self.ui_helper.wait_for_clickable(By.CLASS_NAME, "project-card")
        project_card.click()
        
        # Wait for project detail page to load
        self.ui_helper.wait_for_element(By.TAG_NAME, "h1")
        
        # Click edit button
        edit_button = self.ui_helper.wait_for_clickable(By.XPATH, "//button[contains(text(), 'Edit')]")
        edit_button.click()
        
        # Update status to "Completed"
        status_select = self.ui_helper.wait_for_element(By.ID, "status")
        status_select.click()
        
        completed_option = self.ui_helper.wait_for_clickable(
            By.XPATH, "//option[@value='completed']"
        )
        completed_option.click()
        
        # Update progress to 100%
        progress_input = self.ui_helper.driver.find_element(By.ID, "progress_percentage")
        progress_input.clear()
        progress_input.send_keys("100")
        
        # Submit form
        submit_button = self.ui_helper.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
        
        # Wait for update to complete
        time.sleep(1)
        
        # Verify status is updated
        status_badge = self.ui_helper.wait_for_element(By.CLASS_NAME, "status-badge")
        self.assertIn("Completed", status_badge.text)
        
        print(f"✅ Project status updated to Completed")
    
    def test_05_check_dashboard_stats(self):
        """Test that dashboard statistics reflect challenge and project updates."""
        # Navigate to dashboard
        self.ui_helper.navigate_to("/dashboard")
        
        # Wait for dashboard to load
        self.ui_helper.wait_for_element(By.CLASS_NAME, "dashboard-stats")
        
        # Verify challenge count
        challenge_count_element = self.ui_helper.driver.find_element(
            By.XPATH, "//div[contains(@class, 'stat-card')]//p[contains(text(), 'Challenges')]/..//h3"
        )
        challenge_count = int(challenge_count_element.text)
        self.assertGreaterEqual(challenge_count, 1)
        
        # Verify project count
        project_count_element = self.ui_helper.driver.find_element(
            By.XPATH, "//div[contains(@class, 'stat-card')]//p[contains(text(), 'Projects')]/..//h3"
        )
        project_count = int(project_count_element.text)
        self.assertGreaterEqual(project_count, 1)
        
        # Take screenshot of dashboard
        self.ui_helper.take_screenshot("dashboard_stats")
        
        print(f"✅ Dashboard statistics verified")
    
    def test_06_delete_challenge(self):
        """Test deleting a challenge."""
        # Navigate to the challenge
        self.ui_helper.driver.get(self.__class__.challenge_url)
        
        # Click settings or more options button
        settings_button = self.ui_helper.wait_for_clickable(
            By.XPATH, "//button[contains(@aria-label, 'Settings') or contains(@aria-label, 'More')]"
        )
        settings_button.click()
        
        # Click delete button
        delete_button = self.ui_helper.wait_for_clickable(By.XPATH, "//button[contains(text(), 'Delete')]")
        delete_button.click()
        
        # Confirm deletion
        confirm_button = self.ui_helper.wait_for_clickable(
            By.XPATH, "//button[contains(text(), 'Confirm') or contains(text(), 'Yes')]"
        )
        confirm_button.click()
        
        # Wait for redirect to challenges page
        self.ui_helper.wait_for_element(By.XPATH, "//h1[contains(text(), 'Challenges')]")
        
        # Verify we're on the challenges page
        self.assertTrue("/challenges" in self.ui_helper.driver.current_url)
        
        print(f"✅ Challenge deleted")


if __name__ == "__main__":
    # Run the tests in order
    unittest.main(verbosity=2)
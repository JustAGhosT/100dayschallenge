#!/usr/bin/env python3
"""
Test Automation Setup for 100 Days Challenge Tracker

This script sets up the test automation environment and provides utility functions
for running automated tests.
"""

import os
import sys
import json
import time
import argparse
import unittest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Environment configuration
DEFAULT_FRONTEND_URL = "http://localhost:3000"
DEFAULT_BACKEND_URL = "http://localhost:8888/.netlify/functions"

# Test user credentials
TEST_USER = {
    "email": "test.user@example.com",
    "name": "Test User",
    "picture": "https://example.com/profile.jpg"
}

class TestEnvironment:
    """Manages the test environment configuration."""
    
    def __init__(self):
        """Initialize the test environment."""
        self.frontend_url = os.environ.get("FRONTEND_URL", DEFAULT_FRONTEND_URL)
        self.backend_url = os.environ.get("BACKEND_URL", DEFAULT_BACKEND_URL)
        self.browser = os.environ.get("TEST_BROWSER", "chrome")
        self.headless = os.environ.get("HEADLESS", "true").lower() == "true"
        
        print(f"Test Environment:")
        print(f"  Frontend URL: {self.frontend_url}")
        print(f"  Backend URL: {self.backend_url}")
        print(f"  Browser: {self.browser}")
        print(f"  Headless: {self.headless}")
    
    def get_api_url(self, endpoint):
        """Get the full URL for an API endpoint."""
        return f"{self.backend_url}/{endpoint.lstrip('/')}"
    
    def get_frontend_url(self, path):
        """Get the full URL for a frontend path."""
        return f"{self.frontend_url}/{path.lstrip('/')}"


class WebDriverFactory:
    """Factory for creating WebDriver instances."""
    
    @staticmethod
    def create_driver(browser_name, headless=True):
        """Create a WebDriver instance for the specified browser."""
        browser_name = browser_name.lower()
        
        if browser_name == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            return webdriver.Chrome(options=options)
        
        elif browser_name == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            return webdriver.Firefox(options=options)
        
        elif browser_name == "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless")
            return webdriver.Edge(options=options)
        
        elif browser_name == "safari":
            options = SafariOptions()
            # Safari doesn't support headless mode
            return webdriver.Safari(options=options)
        
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")


class APITestHelper:
    """Helper class for API testing."""
    
    def __init__(self, environment):
        """Initialize the API test helper."""
        self.environment = environment
        self.session = requests.Session()
        self.auth_token = None
    
    def login(self, email=TEST_USER["email"], name=TEST_USER["name"]):
        """Log in and get an authentication token."""
        response = self.session.post(
            self.environment.get_api_url("/api/auth/login"),
            json={"email": email, "name": name}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.auth_token = data.get("session_token")
            self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
            return data
        else:
            raise Exception(f"Login failed: {response.status_code} - {response.text}")
    
    def get(self, endpoint):
        """Send a GET request to the API."""
        return self.session.get(self.environment.get_api_url(endpoint))
    
    def post(self, endpoint, data):
        """Send a POST request to the API."""
        return self.session.post(
            self.environment.get_api_url(endpoint),
            json=data
        )
    
    def put(self, endpoint, data):
        """Send a PUT request to the API."""
        return self.session.put(
            self.environment.get_api_url(endpoint),
            json=data
        )
    
    def delete(self, endpoint):
        """Send a DELETE request to the API."""
        return self.session.delete(self.environment.get_api_url(endpoint))


class UITestHelper:
    """Helper class for UI testing."""
    
    def __init__(self, driver, environment):
        """Initialize the UI test helper."""
        self.driver = driver
        self.environment = environment
        self.wait = WebDriverWait(driver, 10)
    
    def navigate_to(self, path):
        """Navigate to a page in the application."""
        url = self.environment.get_frontend_url(path)
        self.driver.get(url)
        return self
    
    def login(self, email=TEST_USER["email"], name=TEST_USER["name"]):
        """Log in through the UI."""
        self.navigate_to("/")
        
        # Click login button
        login_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))
        )
        login_button.click()
        
        # Fill in login form
        email_input = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_input.send_keys(email)
        
        name_input = self.driver.find_element(By.ID, "name")
        name_input.send_keys(name)
        
        # Submit form
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
        
        # Wait for dashboard to load
        self.wait.until(EC.url_contains("/dashboard"))
        
        return self
    
    def create_challenge(self, title, description, duration=100):
        """Create a new challenge through the UI."""
        self.navigate_to("/challenges")
        
        # Click create challenge button
        create_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create Challenge')]"))
        )
        create_button.click()
        
        # Fill in challenge form
        title_input = self.wait.until(EC.presence_of_element_located((By.ID, "title")))
        title_input.send_keys(title)
        
        description_input = self.driver.find_element(By.ID, "description")
        description_input.send_keys(description)
        
        duration_input = self.driver.find_element(By.ID, "duration_days")
        duration_input.clear()
        duration_input.send_keys(str(duration))
        
        # Submit form
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
        
        # Wait for redirect to challenge page
        self.wait.until(EC.url_contains("/challenges/"))
        
        return self
    
    def create_project(self, title, description, repository_url="", demo_url=""):
        """Create a new project through the UI."""
        # Assume we're on a challenge page
        
        # Click add project button
        add_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Project')]"))
        )
        add_button.click()
        
        # Fill in project form
        title_input = self.wait.until(EC.presence_of_element_located((By.ID, "title")))
        title_input.send_keys(title)
        
        description_input = self.driver.find_element(By.ID, "description")
        description_input.send_keys(description)
        
        if repository_url:
            repo_input = self.driver.find_element(By.ID, "repository_url")
            repo_input.send_keys(repository_url)
        
        if demo_url:
            demo_input = self.driver.find_element(By.ID, "demo_url")
            demo_input.send_keys(demo_url)
        
        # Submit form
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
        
        # Wait for project to be added
        time.sleep(1)
        
        return self
    
    def wait_for_element(self, by, value):
        """Wait for an element to be present."""
        return self.wait.until(EC.presence_of_element_located((by, value)))
    
    def wait_for_clickable(self, by, value):
        """Wait for an element to be clickable."""
        return self.wait.until(EC.element_to_be_clickable((by, value)))
    
    def take_screenshot(self, name):
        """Take a screenshot."""
        screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{screenshot_dir}/{name}_{timestamp}.png"
        
        self.driver.save_screenshot(filename)
        print(f"Screenshot saved: {filename}")
        
        return filename


def setup_test_environment():
    """Set up the test environment."""
    return TestEnvironment()


def setup_api_helper(environment=None):
    """Set up the API test helper."""
    if environment is None:
        environment = setup_test_environment()
    
    return APITestHelper(environment)


def setup_ui_helper(browser="chrome", headless=True, environment=None):
    """Set up the UI test helper."""
    if environment is None:
        environment = setup_test_environment()
    
    driver = WebDriverFactory.create_driver(browser, headless)
    return UITestHelper(driver, environment)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run automated tests for 100 Days Challenge Tracker")
    
    parser.add_argument("--browser", choices=["chrome", "firefox", "edge", "safari"],
                        default="chrome", help="Browser to use for UI tests")
    
    parser.add_argument("--headless", action="store_true", default=True,
                        help="Run browser in headless mode")
    
    parser.add_argument("--frontend-url", default=DEFAULT_FRONTEND_URL,
                        help="URL of the frontend application")
    
    parser.add_argument("--backend-url", default=DEFAULT_BACKEND_URL,
                        help="URL of the backend API")
    
    parser.add_argument("--test-type", choices=["api", "ui", "all"],
                        default="all", help="Type of tests to run")
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    # Set environment variables from arguments
    os.environ["FRONTEND_URL"] = args.frontend_url
    os.environ["BACKEND_URL"] = args.backend_url
    os.environ["TEST_BROWSER"] = args.browser
    os.environ["HEADLESS"] = str(args.headless).lower()
    
    # Setup test environment
    env = setup_test_environment()
    
    # Example usage
    if args.test_type in ["api", "all"]:
        print("\nRunning API tests...")
        api_helper = setup_api_helper(env)
        user_data = api_helper.login()
        print(f"Logged in as: {user_data['user']['name']}")
        
        # Get health status
        health_response = api_helper.get("/api/health")
        print(f"API Health: {health_response.json()}")
    
    if args.test_type in ["ui", "all"]:
        print("\nRunning UI tests...")
        ui_helper = setup_ui_helper(args.browser, args.headless, env)
        
        try:
            ui_helper.navigate_to("/")
            print(f"Page title: {ui_helper.driver.title}")
            
            ui_helper.login()
            print("Logged in successfully")
            
            ui_helper.take_screenshot("dashboard")
        finally:
            ui_helper.driver.quit()
    
    print("\nTest setup complete!")
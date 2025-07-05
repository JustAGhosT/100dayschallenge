#!/usr/bin/env python3
import unittest
import requests
import json
import time
import os
import pymongo
import uuid
from datetime import datetime, timedelta

# Get the backend URL from frontend/.env
with open('/app/frontend/.env', 'r') as f:
    for line in f:
        if line.startswith('REACT_APP_BACKEND_URL='):
            BACKEND_URL = line.strip().split('=')[1].strip('"\'')
            break

API_URL = f"{BACKEND_URL}/api"
print(f"Testing backend at: {API_URL}")

# Get MongoDB connection info from backend/.env
with open('/app/backend/.env', 'r') as f:
    env_vars = {}
    for line in f:
        if '=' in line:
            key, value = line.strip().split('=', 1)
            env_vars[key] = value.strip('"\'')

MONGO_URL = env_vars.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = env_vars.get('DB_NAME', 'test_database')

# Connect to MongoDB directly for test setup
mongo_client = pymongo.MongoClient(MONGO_URL)
db = mongo_client[DB_NAME]

# Test data
TEST_USER = {
    "id": str(uuid.uuid4()),
    "email": "test.user@example.com",
    "name": "Test User",
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

class BackendTests(unittest.TestCase):
    """Test suite for Challenge Tracker Platform backend APIs"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment once before all tests"""
        # Create test user and session in database
        db.users.delete_many({"email": TEST_USER["email"]})
        db.users.insert_one(TEST_USER)
        db.sessions.insert_one(TEST_SESSION)
        
        # Store auth token for all tests
        cls.auth_token = TEST_SESSION["session_token"]
        cls.user_id = TEST_USER["id"]
        print(f"✅ Created test user and session in database")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        # Clean up test data
        db.users.delete_many({"id": cls.user_id})
        db.sessions.delete_many({"user_id": cls.user_id})
        db.challenges.delete_many({"user_id": cls.user_id})
        db.projects.delete_many({"user_id": cls.user_id})
        print(f"✅ Cleaned up test data from database")
    
    def test_01_health_check(self):
        """Test the health check endpoint"""
        response = requests.get(f"{API_URL}/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("timestamp", data)
        print("✅ Health check endpoint is working")
    
    def test_02_create_challenge(self):
        """Test creating a new challenge"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        challenge_data = {
            "title": "30-Day Coding Challenge",
            "description": "Build a new project every day for 30 days",
            "goals": ["Improve coding skills", "Build portfolio", "Learn new technologies"],
            "rules": ["Must commit code daily", "Each project must be unique"],
            "duration_days": 30
        }
        
        response = requests.post(
            f"{API_URL}/challenges", 
            headers=headers,
            json=challenge_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], challenge_data["title"])
        self.assertEqual(data["description"], challenge_data["description"])
        self.assertEqual(data["goals"], challenge_data["goals"])
        self.assertEqual(data["rules"], challenge_data["rules"])
        self.assertEqual(data["duration_days"], challenge_data["duration_days"])
        self.assertIn("start_date", data)
        self.assertIn("end_date", data)
        
        # Save the challenge ID for subsequent tests
        BackendTests.challenge_id = data["id"]
        print(f"✅ Create challenge endpoint is working, created challenge ID: {BackendTests.challenge_id}")
    
    def test_03_get_challenges(self):
        """Test getting all challenges for the user"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = requests.get(f"{API_URL}/challenges", headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)  # Should have at least the one we created
        
        # Verify the challenge we created is in the list
        challenge_ids = [challenge["id"] for challenge in data]
        self.assertIn(BackendTests.challenge_id, challenge_ids)
        print("✅ Get challenges endpoint is working")
    
    def test_04_get_challenge_by_id(self):
        """Test getting a specific challenge by ID"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = requests.get(
            f"{API_URL}/challenges/{BackendTests.challenge_id}", 
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], BackendTests.challenge_id)
        print("✅ Get challenge by ID endpoint is working")
    
    def test_05_update_challenge(self):
        """Test updating a challenge"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        update_data = {
            "title": "Updated 30-Day Coding Challenge",
            "description": "Updated description for the challenge",
            "goals": ["Updated goal 1", "Updated goal 2"],
            "rules": ["Updated rule 1", "Updated rule 2"],
            "duration_days": 45
        }
        
        response = requests.put(
            f"{API_URL}/challenges/{BackendTests.challenge_id}", 
            headers=headers,
            json=update_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], BackendTests.challenge_id)
        self.assertEqual(data["title"], update_data["title"])
        self.assertEqual(data["description"], update_data["description"])
        self.assertEqual(data["goals"], update_data["goals"])
        self.assertEqual(data["rules"], update_data["rules"])
        self.assertEqual(data["duration_days"], update_data["duration_days"])
        print("✅ Update challenge endpoint is working")
    
    def test_06_create_project(self):
        """Test creating a new project within a challenge"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        project_data = {
            "title": "Personal Portfolio Website",
            "description": "A responsive portfolio website showcasing my projects",
            "repository_url": "https://github.com/testuser/portfolio",
            "demo_url": "https://portfolio-demo.example.com",
            "tech_stack": ["React", "Tailwind CSS", "Node.js"],
            "status": "in_progress"
        }
        
        response = requests.post(
            f"{API_URL}/challenges/{BackendTests.challenge_id}/projects", 
            headers=headers,
            json=project_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["challenge_id"], BackendTests.challenge_id)
        self.assertEqual(data["title"], project_data["title"])
        self.assertEqual(data["description"], project_data["description"])
        self.assertEqual(data["repository_url"], project_data["repository_url"])
        self.assertEqual(data["demo_url"], project_data["demo_url"])
        self.assertEqual(data["tech_stack"], project_data["tech_stack"])
        self.assertEqual(data["status"], project_data["status"])
        
        # Save the project ID for subsequent tests
        BackendTests.project_id = data["id"]
        print(f"✅ Create project endpoint is working, created project ID: {BackendTests.project_id}")
    
    def test_07_get_challenge_projects(self):
        """Test getting all projects for a challenge"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = requests.get(
            f"{API_URL}/challenges/{BackendTests.challenge_id}/projects", 
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)  # Should have at least the one we created
        
        # Verify the project we created is in the list
        project_ids = [project["id"] for project in data]
        self.assertIn(BackendTests.project_id, project_ids)
        print("✅ Get challenge projects endpoint is working")
    
    def test_08_get_project_by_id(self):
        """Test getting a specific project by ID"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = requests.get(
            f"{API_URL}/projects/{BackendTests.project_id}", 
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], BackendTests.project_id)
        print("✅ Get project by ID endpoint is working")
    
    def test_09_update_project(self):
        """Test updating a project"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        update_data = {
            "title": "Updated Portfolio Website",
            "description": "Updated description for the portfolio project",
            "repository_url": "https://github.com/testuser/updated-portfolio",
            "demo_url": "https://updated-portfolio.example.com",
            "tech_stack": ["React", "Tailwind CSS", "Node.js", "MongoDB"],
            "status": "completed",
            "progress_percentage": 100
        }
        
        response = requests.put(
            f"{API_URL}/projects/{BackendTests.project_id}", 
            headers=headers,
            json=update_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], BackendTests.project_id)
        self.assertEqual(data["title"], update_data["title"])
        self.assertEqual(data["description"], update_data["description"])
        self.assertEqual(data["repository_url"], update_data["repository_url"])
        self.assertEqual(data["demo_url"], update_data["demo_url"])
        self.assertEqual(data["tech_stack"], update_data["tech_stack"])
        self.assertEqual(data["status"], update_data["status"])
        self.assertEqual(data["progress_percentage"], update_data["progress_percentage"])
        print("✅ Update project endpoint is working")
    
    def test_10_check_url_monitoring(self):
        """Test URL monitoring background job"""
        # Wait a bit for the background job to complete
        time.sleep(2)
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = requests.get(
            f"{API_URL}/projects/{BackendTests.project_id}", 
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check if URL monitoring data is present
        self.assertIn("url_status", data)
        self.assertIn("last_url_check", data)
        
        # If URLs were provided, there should be status info
        if data["repository_url"] or data["demo_url"]:
            self.assertIsNotNone(data["last_url_check"])
            
            if data["repository_url"]:
                self.assertIn("repository", data["url_status"])
                self.assertEqual(data["url_status"]["repository"]["url"], data["repository_url"])
            
            if data["demo_url"]:
                self.assertIn("demo", data["url_status"])
                self.assertEqual(data["url_status"]["demo"]["url"], data["demo_url"])
        
        print("✅ URL monitoring background job is working")
    
    def test_11_dashboard_analytics(self):
        """Test dashboard analytics endpoint"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = requests.get(f"{API_URL}/dashboard", headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check dashboard structure
        self.assertIn("user", data)
        self.assertIn("stats", data)
        self.assertIn("recent_challenges", data)
        self.assertIn("recent_projects", data)
        self.assertIn("tech_stack_distribution", data)
        
        # Check stats
        stats = data["stats"]
        self.assertIn("total_challenges", stats)
        self.assertIn("active_challenges", stats)
        self.assertIn("completed_challenges", stats)
        self.assertIn("total_projects", stats)
        self.assertIn("completed_projects", stats)
        self.assertIn("overall_progress", stats)
        
        # Verify we have at least the challenge and project we created
        self.assertGreaterEqual(stats["total_challenges"], 1)
        self.assertGreaterEqual(stats["total_projects"], 1)
        
        # Check tech stack distribution
        tech_stack = data["tech_stack_distribution"]
        for tech in ["React", "Tailwind CSS", "Node.js", "MongoDB"]:
            self.assertIn(tech, tech_stack)
        
        print("✅ Dashboard analytics endpoint is working")
    
    def test_12_delete_project(self):
        """Test deleting a project"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = requests.delete(
            f"{API_URL}/projects/{BackendTests.project_id}", 
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Project deleted successfully")
        print("✅ Delete project endpoint is working")
        
        # Verify the project is actually deleted
        response = requests.get(
            f"{API_URL}/projects/{BackendTests.project_id}", 
            headers=headers
        )
        self.assertEqual(response.status_code, 404)
        print("✅ Project deletion confirmed")


if __name__ == "__main__":
    # Run the tests in order
    unittest.main(verbosity=2)
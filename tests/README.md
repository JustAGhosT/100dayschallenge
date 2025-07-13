# Challenge Tracker Platform Tests

This directory contains automated tests for the Challenge Tracker Platform.

## Test Types

1. **Backend Tests** (`backend_test.py`): Tests the backend API endpoints and database interactions.
2. **Frontend Tests** (`frontend_test.py`): Tests the frontend UI using Selenium WebDriver.
3. **Integration Tests** (`integration_test.py`): Tests the interaction between frontend and backend.

## Running Tests

You can run the tests using the `run_tests.py` script:

```bash
# Run all tests
python tests/run_tests.py

# Run only backend tests
python tests/run_tests.py --type backend

# Run only frontend tests
python tests/run_tests.py --type frontend

# Run only integration tests
python tests/run_tests.py --type integration

# Run with verbose output
python tests/run_tests.py --verbose
```

## Test Results

Test results are saved to `test_result.md` in the project root directory.

## Environment Variables

The tests use the following environment variables:

- `FRONTEND_URL`: URL of the frontend application (default: http://localhost:3000)
- `BACKEND_URL`: URL of the backend API (default: http://localhost:5000)
- `MONGO_URL`: MongoDB connection string (default: mongodb://localhost:27017)
- `DB_NAME`: MongoDB database name (default: test_database)

## Prerequisites

1. Python 3.6+
2. Required Python packages:
   - unittest
   - requests
   - pymongo
   - selenium
   - webdriver-manager

3. Chrome browser (for UI tests)

## Installing Dependencies

```bash
pip install -r requirements.txt
```

## Docker Setup

You can also run the tests in Docker:

```bash
# Build the test container
docker build -f tests/Dockerfile -t challenge-tracker-tests .

# Run all tests
docker run challenge-tracker-tests

# Run specific test type
docker run challenge-tracker-tests --type backend
```
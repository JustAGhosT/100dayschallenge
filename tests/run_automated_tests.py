#!/usr/bin/env python3
"""
Test Runner for 100 Days Challenge Tracker

This script runs automated tests for the 100 Days Challenge Tracker application.
"""

import os
import sys
import argparse
import unittest
import time
from datetime import datetime

# Add automation directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import test modules
from automation.test_automation_setup import setup_test_environment

def discover_and_run_tests(test_type=None, browser="chrome", headless=True, 
                          frontend_url=None, backend_url=None, verbosity=1):
    """Discover and run tests based on type."""
    # Set environment variables
    if frontend_url:
        os.environ["FRONTEND_URL"] = frontend_url
    if backend_url:
        os.environ["BACKEND_URL"] = backend_url
    
    os.environ["TEST_BROWSER"] = browser
    os.environ["HEADLESS"] = str(headless).lower()
    
    # Setup test environment
    env = setup_test_environment()
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Discover tests based on type
    if test_type in [None, "all", "ui"]:
        ui_tests = unittest.defaultTestLoader.discover(
            os.path.join(os.path.dirname(__file__), "automation"),
            pattern="test_*.py"
        )
        test_suite.addTest(ui_tests)
    
    if test_type in [None, "all", "api"]:
        api_tests = unittest.defaultTestLoader.discover(
            os.path.join(os.path.dirname(__file__)),
            pattern="backend_test.py"
        )
        test_suite.addTest(api_tests)
    
    if test_type in [None, "all", "integration"]:
        integration_tests = unittest.defaultTestLoader.discover(
            os.path.join(os.path.dirname(__file__)),
            pattern="integration_test.py"
        )
        test_suite.addTest(integration_tests)
    
    # Run tests
    start_time = time.time()
    print(f"Starting tests at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(test_suite)
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Print summary
    print("\n" + "="*80)
    print(f"Test Summary:")
    print(f"  - Run Duration: {duration:.2f} seconds")
    print(f"  - Tests Run: {result.testsRun}")
    print(f"  - Errors: {len(result.errors)}")
    print(f"  - Failures: {len(result.failures)}")
    print(f"  - Skipped: {len(result.skipped)}")
    print("="*80)
    
    # Generate test report
    report_file = os.path.join(os.path.dirname(__file__), "test_result.md")
    with open(report_file, "w") as f:
        f.write(f"# Test Results\n\n")
        f.write(f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- **Duration:** {duration:.2f} seconds\n")
        f.write(f"- **Tests Run:** {result.testsRun}\n")
        f.write(f"- **Errors:** {len(result.errors)}\n")
        f.write(f"- **Failures:** {len(result.failures)}\n")
        f.write(f"- **Skipped:** {len(result.skipped)}\n\n")
        
        if result.failures:
            f.write(f"## Failures\n\n")
            for i, (test, traceback) in enumerate(result.failures):
                f.write(f"### Failure {i+1}: {test}\n\n")
                f.write(f"```\n{traceback}\n```\n\n")
        
        if result.errors:
            f.write(f"## Errors\n\n")
            for i, (test, traceback) in enumerate(result.errors):
                f.write(f"### Error {i+1}: {test}\n\n")
                f.write(f"```\n{traceback}\n```\n\n")
    
    print(f"Test report generated: {report_file}")
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run tests for 100 Days Challenge Tracker")
    
    parser.add_argument("--type", choices=["ui", "api", "integration", "all"],
                        default="all", help="Type of tests to run")
    
    parser.add_argument("--browser", choices=["chrome", "firefox", "edge", "safari"],
                        default="chrome", help="Browser to use for UI tests")
    
    parser.add_argument("--no-headless", action="store_true",
                        help="Run browser in visible mode (not headless)")
    
    parser.add_argument("--frontend-url", 
                        help="URL of the frontend application")
    
    parser.add_argument("--backend-url",
                        help="URL of the backend API")
    
    parser.add_argument("--verbose", "-v", action="count", default=1,
                        help="Increase verbosity (can be used multiple times)")
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    exit_code = discover_and_run_tests(
        test_type=args.type,
        browser=args.browser,
        headless=not args.no_headless,
        frontend_url=args.frontend_url,
        backend_url=args.backend_url,
        verbosity=args.verbose
    )
    
    sys.exit(exit_code)
#!/usr/bin/env python3
import unittest
import os
import sys
import argparse
import time
from datetime import datetime

# Add parent directory to path so we can import test modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import test modules
from tests.backend_test import BackendTests
from tests.frontend_test import FrontendTests
from tests.integration_test import IntegrationTests

def run_tests(test_type=None, verbose=False):
    """Run the specified tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add tests based on type
    if test_type == 'backend' or test_type is None:
        test_suite.addTest(unittest.makeSuite(BackendTests))
    
    if test_type == 'frontend' or test_type is None:
        test_suite.addTest(unittest.makeSuite(FrontendTests))
    
    if test_type == 'integration' or test_type is None:
        test_suite.addTest(unittest.makeSuite(IntegrationTests))
    
    # Run tests
    verbosity = 2 if verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    
    start_time = time.time()
    print(f"Starting tests at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
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
    
    # Write results to file
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_result.md'), 'w') as f:
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
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Challenge Tracker Platform tests')
    parser.add_argument('--type', choices=['backend', 'frontend', 'integration'], 
                        help='Type of tests to run (default: all)')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    sys.exit(run_tests(args.type, args.verbose))
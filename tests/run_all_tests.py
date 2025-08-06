#!/usr/bin/env python3
"""
Test runner for the financial calculator application.

This script discovers and runs all tests in the tests directory.
"""

import unittest
import sys
import os

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def run_all_tests():
    """Discover and run all tests in the tests directory."""
    # Get the directory where this script is located (tests directory)
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Discover all test modules in the tests directory
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    # Run the tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)
#!/usr/bin/env python3
"""
Test runner for the financial calculator project.
This script runs all tests and provides a comprehensive report.
"""

import unittest
import sys
import os

def run_all_tests():
    """Run all tests in the project and return the test results."""
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = current_dir
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Create a test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run the tests
    result = runner.run(suite)
    
    return result

def run_specific_test(test_file):
    """Run a specific test file."""
    if not test_file.endswith('.py'):
        test_file += '.py'
    
    if not os.path.exists(test_file):
        print(f"Error: Test file '{test_file}' not found.")
        return None
    
    # Import and run the specific test
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern=test_file)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result

def main():
    """Main function to run tests based on command line arguments."""
    
    if len(sys.argv) > 1:
        # Run specific test file
        test_file = sys.argv[1]
        print(f"Running specific test: {test_file}")
        result = run_specific_test(test_file)
    else:
        # Run all tests
        print("Running all tests...")
        result = run_all_tests()
    
    if result:
        # Print summary
        print("\n" + "="*50)
        print("TEST SUMMARY")
        print("="*50)
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
        
        if result.failures:
            print("\nFAILURES:")
            for test, traceback in result.failures:
                print(f"  {test}: {traceback}")
        
        if result.errors:
            print("\nERRORS:")
            for test, traceback in result.errors:
                print(f"  {test}: {traceback}")
        
        # Return appropriate exit code
        if result.failures or result.errors:
            print("\n❌ Some tests failed!")
            sys.exit(1)
        else:
            print("\n✅ All tests passed!")
            sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
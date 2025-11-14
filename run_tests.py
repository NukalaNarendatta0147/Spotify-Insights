"""
Test runner script with coverage reporting
"""
import sys
import unittest
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_tests(verbosity=2):
    """Run all tests with specified verbosity"""
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("="*70)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


def run_specific_test(test_module, test_class=None, test_method=None):
    """Run a specific test module, class, or method"""
    if test_method and test_class:
        suite = unittest.TestLoader().loadTestsFromName(
            f'{test_module}.{test_class}.{test_method}'
        )
    elif test_class:
        suite = unittest.TestLoader().loadTestsFromName(
            f'{test_module}.{test_class}'
        )
    else:
        suite = unittest.TestLoader().loadTestsFromName(test_module)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run specific test
        test_path = sys.argv[1]
        parts = test_path.split('.')
        
        if len(parts) == 3:
            exit_code = run_specific_test(parts[0], parts[1], parts[2])
        elif len(parts) == 2:
            exit_code = run_specific_test(parts[0], parts[1])
        else:
            exit_code = run_specific_test(parts[0])
    else:
        # Run all tests
        exit_code = run_tests()
    
    sys.exit(exit_code)

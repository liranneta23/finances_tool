# Testing Documentation

This document describes the testing setup and how to run tests for the financial calculator project.

## Test Structure

The project includes comprehensive tests for all modules:

- `test_investments.py` - Tests for investment calculations
- `test_gifts.py` - Tests for gift tax calculations  
- `test_mortgage.py` - Tests for mortgage calculations
- `test_helper_functions.py` - Tests for utility functions
- `test_main.py` - Tests for the main application flow

## Running Tests

### Run All Tests

```bash
python run_tests.py
```

### Run Specific Test File

```bash
python run_tests.py test_investments
python run_tests.py test_gifts
python run_tests.py test_mortgage
python run_tests.py test_helper_functions
python run_tests.py test_main
```

### Run Tests with Python's unittest

```bash
# Run all tests
python -m unittest discover -v

# Run specific test file
python -m unittest test_investments -v
python -m unittest test_gifts -v
python -m unittest test_mortgage -v
python -m unittest test_helper_functions -v
python -m unittest test_main -v

# Run specific test method
python -m unittest test_investments.TestInvestments.test_calculate_principal -v
```

## Test Coverage

### Investment Tests (`test_investments.py`)
- ✅ `calculate_principal()` - Basic calculations and edge cases
- ✅ `calculate_growth_over_n_years()` - Growth calculations with various yields
- ✅ `calculate_monthly_required_to_reach_z()` - Monthly investment calculations
- ✅ `total_return()` - End-to-end investment return calculation
- ✅ `find_how_much_to_invest()` - Monthly investment requirement calculation
- ✅ Edge cases and boundary conditions

### Gift Tests (`test_gifts.py`)
- ✅ `calculate_gift_tax()` - Tax calculations for different brackets
- ✅ `gift_tax_net()` - Net amount calculations
- ✅ `gift_calculations()` - End-to-end gift calculation flow
- ✅ Exemption thresholds and tax brackets
- ✅ Real-world examples and edge cases

### Mortgage Tests (`test_mortgage.py`)
- ✅ `find_portion_key()` - Portion classification logic
- ✅ `find_year_key()` - Year classification logic
- ✅ `find_interest_rate()` - Interest rate lookup
- ✅ `calculate_total_linear_interest()` - Linear mortgage interest calculations
- ✅ `calculate_dutch_linear_mortgage()` - Dutch linear mortgage calculations
- ✅ `linear_mortgage()` - Linear mortgage output formatting
- ✅ `calculate_annuity_mortgage_payment()` - Annuity payment calculations
- ✅ `calculate_total_annuity_interest()` - Annuity interest calculations
- ✅ `annuity_mortgage()` - Annuity mortgage output formatting
- ✅ Edge cases and interest rate consistency

### Helper Function Tests (`test_helper_functions.py`)
- ✅ `decimal_to_percentage()` - Decimal to percentage conversion
- ✅ Rounding behavior and edge cases
- ✅ Real-world investment scenarios

### Main Application Tests (`test_main.py`)
- ✅ Menu display and navigation
- ✅ Input validation and error handling
- ✅ Function mapping and structure validation

## Test Features

### Mocking
Tests use Python's `unittest.mock` to:
- Mock user input (`@patch('builtins.input')`)
- Capture and verify console output (`@patch('sys.stdout')`)
- Test interactive functions without user input

### Edge Cases
All tests include edge cases such as:
- Zero values and very small numbers
- Very large numbers
- Boundary conditions
- Invalid inputs and error handling

### Real-world Examples
Tests include realistic scenarios:
- Common investment returns (5%, 7%, 10%)
- Typical mortgage amounts and terms
- Realistic gift amounts and tax brackets

## Test Output

When running tests, you'll see:
- Individual test results with pass/fail status
- Detailed error messages for failures
- Test summary with counts of tests run, failures, and errors
- Exit codes for CI/CD integration

## Continuous Integration

The test suite is designed to work with CI/CD systems:
- Exit code 0 for all tests passing
- Exit code 1 for any test failures
- Comprehensive error reporting
- No external dependencies required

## Adding New Tests

To add tests for new functionality:

1. Create a new test file following the naming convention `test_<module>.py`
2. Import the functions to test
3. Create test classes inheriting from `unittest.TestCase`
4. Write test methods with descriptive names
5. Include edge cases and error conditions
6. Use mocking for interactive functions

Example:
```python
import unittest
from unittest.mock import patch
from your_module import your_function

class TestYourModule(unittest.TestCase):
    def test_your_function_basic(self):
        result = your_function(10)
        self.assertEqual(result, expected_value)
    
    @patch('builtins.input', return_value='test')
    def test_your_function_with_input(self, mock_input):
        # Test interactive function
        pass
```

## Best Practices

- Test both valid and invalid inputs
- Include edge cases and boundary conditions
- Use descriptive test method names
- Mock external dependencies and user input
- Test error conditions and exception handling
- Keep tests independent and isolated
- Use appropriate assertions for different data types
# Test Suite for Financial Calculator

This document describes the comprehensive test suite for the Financial Calculator application.

## Overview

The test suite covers all core functionality of the financial calculator, including:

- **Investment calculations** - Testing compound growth, principal calculations, and monthly investment requirements
- **Gift tax calculations** - Testing Dutch gift tax calculations with different brackets and exemptions
- **Mortgage calculations** - Testing both linear and annuity mortgage calculations, interest rate lookups
- **Helper functions** - Testing utility functions like decimal to percentage conversion
- **Constants validation** - Testing that all interest rate data is valid and follows expected patterns

## Test Structure

```
tests/
├── __init__.py                 # Makes tests a Python package
├── run_all_tests.py           # Main test runner script
├── test_constants.py          # Tests for constants.py
├── test_gifts.py              # Tests for gifts.py
├── test_helper_functions.py   # Tests for helper_functions.py
├── test_investments.py        # Tests for investments.py
└── test_mortgage.py           # Tests for mortgage.py
```

## Running Tests

### Run All Tests

To run the complete test suite:

```bash
# From the project root directory
python tests/run_all_tests.py
```

### Run Individual Test Modules

To run tests for a specific module:

```bash
# From the project root directory
python -m unittest tests.test_gifts
python -m unittest tests.test_investments
python -m unittest tests.test_mortgage
python -m unittest tests.test_helper_functions
python -m unittest tests.test_constants
```

### Run Specific Test Cases

To run a specific test case:

```bash
python -m unittest tests.test_gifts.TestGifts.test_calculate_gift_tax_no_tax
```

### Verbose Output

For more detailed output, add the `-v` flag:

```bash
python -m unittest tests.test_gifts -v
```

## Test Coverage

### Investment Tests (`test_investments.py`)
- **Principal calculations** - Basic multiplication of annual amount by years
- **Growth calculations** - Compound interest calculations over multiple years
- **Monthly investment requirements** - Reverse calculations to reach target amounts
- **Edge cases** - Zero values, large amounts, small yields
- **Mathematical relationships** - Verification that functions work together correctly

### Gift Tax Tests (`test_gifts.py`)
- **Tax-free scenarios** - Amounts below exemption thresholds
- **First tax bracket** - 10% tax on amounts above exemptions
- **Second tax bracket** - 20% tax on high amounts
- **Boundary conditions** - Exact bracket limits and transitions
- **Net amount calculations** - After-tax gift amounts

### Mortgage Tests (`test_mortgage.py`)
- **Interest rate lookups** - Correct rates for different LTV ratios and terms
- **Linear mortgage calculations** - Decreasing payment schedules
- **Annuity mortgage calculations** - Fixed payment schedules
- **Tax deduction calculations** - Dutch mortgage interest deductions
- **Edge cases** - Small amounts, long terms, zero interest rates
- **Mathematical correctness** - Verification against standard formulas

### Helper Function Tests (`test_helper_functions.py`)
- **Decimal to percentage conversion** - Various input ranges
- **Precision handling** - Rounding behavior
- **Edge cases** - Negative percentages, large values

### Constants Tests (`test_constants.py`)
- **Data structure validation** - All required keys present
- **Rate reasonableness** - Values within expected ranges
- **Risk premium logic** - Higher LTV ratios have higher rates
- **Data completeness** - All combinations of terms and LTV ratios covered

## Test Principles

### Comprehensive Coverage
- Each public function has multiple test cases
- Edge cases and boundary conditions are explicitly tested
- Both valid inputs and error conditions are covered

### Mathematical Accuracy
- Financial calculations are verified against known formulas
- Cross-validation between related functions
- Precision and rounding behavior is tested

### Real-world Scenarios
- Test cases use realistic financial values
- Dutch tax and mortgage rules are properly validated
- Constants reflect actual market conditions

### Maintainability
- Clear test names describing what is being tested
- Comprehensive docstrings explaining test purposes
- Modular structure allowing easy addition of new tests

## Adding New Tests

When adding new functionality to the calculator:

1. **Create corresponding test cases** - Follow the existing naming pattern `test_module_name.py`
2. **Test all code paths** - Include normal cases, edge cases, and error conditions
3. **Use descriptive test names** - Method names should clearly indicate what is being tested
4. **Add documentation** - Include docstrings explaining the test purpose
5. **Update this README** - Document any new test categories or requirements

## Continuous Integration

The test suite is designed to be easily integrated with CI/CD systems:

- **Exit codes** - Test runner returns 0 for success, 1 for failures
- **No external dependencies** - Uses only Python standard library
- **Fast execution** - All tests complete in seconds
- **Detailed output** - Clear reporting of failures and errors

## Example Test Output

```
test_calculate_gift_tax_first_bracket (tests.test_gifts.TestGifts) ... ok
test_calculate_gift_tax_no_tax (tests.test_gifts.TestGifts) ... ok
test_calculate_gift_tax_second_bracket (tests.test_gifts.TestGifts) ... ok
test_calculate_principal_basic (tests.test_investments.TestInvestments) ... ok
test_find_interest_rate_integration (tests.test_mortgage.TestMortgage) ... ok

----------------------------------------------------------------------
Ran 45 tests in 0.123s

OK
```

## Troubleshooting

### Import Errors
If you encounter import errors, ensure you're running tests from the project root directory:
```bash
cd /path/to/financial-calculator
python tests/run_all_tests.py
```

### Path Issues
The test files automatically add the parent directory to the Python path, but if you encounter issues, you can manually set the PYTHONPATH:
```bash
export PYTHONPATH=/path/to/financial-calculator:$PYTHONPATH
python tests/run_all_tests.py
```

### Python Version
The tests are compatible with Python 3.6+ and use only standard library modules.
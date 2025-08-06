import unittest
import sys
import os

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mortgage import (
    find_portion_key,
    find_year_key,
    find_interest_rate,
    calculate_total_linear_interest,
    calculate_dutch_linear_mortgage,
    calculate_annuity_mortgage_payment,
    calculate_total_annuity_interest,
    MONTHS_IN_YEAR
)
from constants import interest_rates


class TestMortgage(unittest.TestCase):
    """Test cases for mortgage.py"""

    def test_find_portion_key_nhg(self):
        """Test find_portion_key with NHG input"""
        self.assertEqual(find_portion_key("NHG"), "NHG")

    def test_find_portion_key_percentages(self):
        """Test find_portion_key with percentage inputs"""
        self.assertEqual(find_portion_key(0.50), "≤65%")
        self.assertEqual(find_portion_key(0.65), "≤65%")
        self.assertEqual(find_portion_key(0.70), "≤85%")
        self.assertEqual(find_portion_key(0.85), "≤85%")
        self.assertEqual(find_portion_key(0.87), "≤90%")
        self.assertEqual(find_portion_key(0.90), "≤90%")
        self.assertEqual(find_portion_key(0.95), ">90%")
        self.assertEqual(find_portion_key(1.0), ">90%")

    def test_find_portion_key_edge_cases(self):
        """Test find_portion_key edge cases"""
        self.assertEqual(find_portion_key(0.01), "≤65%")  # Very small positive
        self.assertEqual(find_portion_key(0.650001), "≤85%")  # Just above 65%
        self.assertEqual(find_portion_key(0.850001), "≤90%")  # Just above 85%
        self.assertEqual(find_portion_key(0.900001), ">90%")  # Just above 90%

    def test_find_portion_key_invalid(self):
        """Test find_portion_key with invalid inputs"""
        with self.assertRaises(ValueError):
            find_portion_key(0)
        with self.assertRaises(ValueError):
            find_portion_key(-0.1)
        with self.assertRaises(ValueError):
            find_portion_key(1.1)
        with self.assertRaises((ValueError, TypeError)):
            find_portion_key("invalid")

    def test_find_year_key_ranges(self):
        """Test find_year_key with different year ranges"""
        self.assertEqual(find_year_key(0.5), "Variable")
        self.assertEqual(find_year_key(1), "Variable")
        self.assertEqual(find_year_key(3), "5")
        self.assertEqual(find_year_key(5), "5")
        self.assertEqual(find_year_key(7), "10")
        self.assertEqual(find_year_key(10), "10")
        self.assertEqual(find_year_key(12), "15")
        self.assertEqual(find_year_key(15), "15")
        self.assertEqual(find_year_key(18), "20")
        self.assertEqual(find_year_key(20), "20")
        self.assertEqual(find_year_key(25), "30")
        self.assertEqual(find_year_key(30), "30")

    def test_find_year_key_edge_cases(self):
        """Test find_year_key edge cases"""
        # Negative years return "Variable" (function doesn't raise ValueError)
        self.assertEqual(find_year_key(-1), "Variable")
        self.assertEqual(find_year_key(0), "Variable")
        self.assertEqual(find_year_key(0.5), "Variable")

    def test_find_interest_rate_integration(self):
        """Test find_interest_rate function integration"""
        # Test with known values from constants
        rate = find_interest_rate(5, 0.6)  # 5 years, 60% LTV
        expected = interest_rates["5"]["≤65%"]
        self.assertEqual(rate, expected)
        
        rate = find_interest_rate(25, "NHG")  # 25 years, NHG
        expected = interest_rates["30"]["NHG"]
        self.assertEqual(rate, expected)

    def test_calculate_total_linear_interest_basic(self):
        """Test basic linear interest calculation"""
        total_interest, total_tax_return = calculate_total_linear_interest(100000, 0.04, 10)
        
        # Total interest should be positive
        self.assertGreater(total_interest, 0)
        self.assertGreater(total_tax_return, 0)
        
        # Tax return should be less than total interest
        self.assertLess(total_tax_return, total_interest)

    def test_calculate_total_linear_interest_zero_rate(self):
        """Test linear interest calculation with zero interest rate"""
        total_interest, total_tax_return = calculate_total_linear_interest(100000, 0.0, 10)
        
        self.assertEqual(total_interest, 0.0)
        self.assertEqual(total_tax_return, 0.0)

    def test_calculate_dutch_linear_mortgage_structure(self):
        """Test dutch linear mortgage calculation returns correct structure"""
        result = calculate_dutch_linear_mortgage(200000, 0.04, 20)
        
        # Should return 5 values
        self.assertEqual(len(result), 5)
        
        initial_payment, final_payment, mortgage_amount, total_interest, total_tax_return = result
        
        # Initial payment should be higher than final payment (linear mortgage characteristic)
        self.assertGreater(initial_payment, final_payment)
        
        # Mortgage amount should match input
        self.assertEqual(mortgage_amount, 200000)
        
        # All values should be positive
        self.assertGreater(initial_payment, 0)
        self.assertGreater(final_payment, 0)
        self.assertGreater(total_interest, 0)
        self.assertGreater(total_tax_return, 0)

    def test_calculate_dutch_linear_mortgage_mathematical_correctness(self):
        """Test mathematical correctness of dutch linear mortgage"""
        mortgage_amount = 100000
        interest_rate = 0.04
        years = 10
        
        initial_payment, final_payment, _, total_interest, _ = calculate_dutch_linear_mortgage(
            mortgage_amount, interest_rate, years)
        
        # Calculate expected monthly principal
        expected_monthly_principal = mortgage_amount / (years * MONTHS_IN_YEAR)
        
        # Initial monthly interest
        expected_initial_interest = (mortgage_amount * interest_rate) / MONTHS_IN_YEAR
        expected_initial_payment = expected_monthly_principal + expected_initial_interest
        
        # Final monthly interest (on last principal payment)
        expected_final_interest = (expected_monthly_principal * interest_rate) / MONTHS_IN_YEAR
        expected_final_payment = expected_monthly_principal + expected_final_interest
        
        self.assertAlmostEqual(initial_payment, expected_initial_payment, places=2)
        self.assertAlmostEqual(final_payment, expected_final_payment, places=2)

    def test_calculate_annuity_mortgage_payment_basic(self):
        """Test basic annuity mortgage payment calculation"""
        payment = calculate_annuity_mortgage_payment(100000, 0.04, 20)
        
        # Payment should be positive
        self.assertGreater(payment, 0)
        
        # Payment should be reasonable (less than principal/months but more than principal only)
        principal_only = 100000 / (20 * MONTHS_IN_YEAR)
        self.assertGreater(payment, principal_only)

    def test_calculate_annuity_mortgage_payment_zero_rate(self):
        """Test annuity mortgage payment with zero interest rate"""
        payment = calculate_annuity_mortgage_payment(100000, 0.0, 20)
        expected_payment = 100000 / (20 * MONTHS_IN_YEAR)
        
        self.assertEqual(payment, expected_payment)

    def test_calculate_annuity_mortgage_payment_mathematical_formula(self):
        """Test annuity payment calculation against mathematical formula"""
        principal = 100000
        annual_rate = 0.04
        years = 15
        
        monthly_rate = annual_rate / MONTHS_IN_YEAR
        num_payments = years * MONTHS_IN_YEAR
        
        # Calculate expected payment using standard annuity formula
        expected_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / (
                (1 + monthly_rate) ** num_payments - 1)
        
        actual_payment = calculate_annuity_mortgage_payment(principal, annual_rate, years)
        
        self.assertAlmostEqual(actual_payment, expected_payment, places=6)

    def test_calculate_total_annuity_interest_structure(self):
        """Test annuity interest calculation returns correct structure"""
        total_paid = 150000
        monthly_payment = 500
        mortgage_amount = 100000
        interest_rate = 0.04
        years = 20
        
        total_interest, total_tax_return = calculate_total_annuity_interest(
            total_paid, monthly_payment, mortgage_amount, interest_rate, years)
        
        # Total interest should equal total paid minus principal
        expected_total_interest = total_paid - mortgage_amount
        self.assertEqual(total_interest, expected_total_interest)
        
        # Tax return should be positive and less than total interest
        self.assertGreater(total_tax_return, 0)
        self.assertLess(total_tax_return, total_interest)

    def test_mortgage_constants(self):
        """Test mortgage-related constants"""
        self.assertEqual(MONTHS_IN_YEAR, 12)

    def test_edge_cases_small_amounts(self):
        """Test edge cases with small mortgage amounts"""
        # Small mortgage amount
        result = calculate_dutch_linear_mortgage(10000, 0.03, 5)
        self.assertEqual(len(result), 5)
        
        # All values should still be positive
        for value in result:
            self.assertGreaterEqual(value, 0)

    def test_edge_cases_long_periods(self):
        """Test edge cases with long mortgage periods"""
        # Long mortgage period
        result = calculate_dutch_linear_mortgage(200000, 0.04, 30)
        initial_payment, final_payment, _, _, _ = result
        
        # Should still have decreasing payments characteristic
        self.assertGreater(initial_payment, final_payment)

    def test_comparison_linear_vs_annuity_characteristics(self):
        """Test that linear and annuity mortgages have expected characteristics"""
        mortgage_amount = 200000
        interest_rate = 0.04
        years = 20
        
        # Linear mortgage
        linear_initial, linear_final, _, linear_total_interest, _ = calculate_dutch_linear_mortgage(
            mortgage_amount, interest_rate, years)
        
        # Annuity mortgage
        annuity_payment = calculate_annuity_mortgage_payment(mortgage_amount, interest_rate, years)
        
        # Linear mortgage: initial payment should be higher than annuity payment
        # but final payment should be lower
        self.assertGreater(linear_initial, annuity_payment)
        self.assertLess(linear_final, annuity_payment)


if __name__ == '__main__':
    unittest.main()
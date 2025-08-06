import unittest
import sys
import os

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from investments import (
    calculate_principal,
    calculate_growth_over_n_years,
    calculate_monthly_required_to_reach_z
)


class TestInvestments(unittest.TestCase):
    """Test cases for investments.py"""

    def test_calculate_principal_basic(self):
        """Test basic principal calculation"""
        self.assertEqual(calculate_principal(1000, 5), 5000)
        self.assertEqual(calculate_principal(500, 10), 5000)
        self.assertEqual(calculate_principal(0, 5), 0)
        self.assertEqual(calculate_principal(1000, 0), 0)

    def test_calculate_principal_edge_cases(self):
        """Test edge cases for principal calculation"""
        # Fractional values
        self.assertEqual(calculate_principal(1000.5, 2), 2001.0)
        self.assertEqual(calculate_principal(1000, 2.5), 2500.0)
        
        # Large values
        self.assertEqual(calculate_principal(10000, 20), 200000)

    def test_calculate_growth_over_n_years_no_growth(self):
        """Test growth calculation with 0% yield"""
        growth = calculate_growth_over_n_years(0.0, 5)
        self.assertEqual(growth, 1.0)  # No growth means multiplier of 1

    def test_calculate_growth_over_n_years_positive_yield(self):
        """Test growth calculation with positive yield"""
        # 10% yield for 1 year should be 1.1
        growth = calculate_growth_over_n_years(0.1, 1)
        self.assertAlmostEqual(growth, 1.1, places=2)
        
        # 10% yield for 2 years: (1.1 + 1.21) / 2 = 1.155
        growth = calculate_growth_over_n_years(0.1, 2)
        expected = (1.1 + 1.21) / 2
        self.assertAlmostEqual(growth, expected, places=6)

    def test_calculate_growth_over_n_years_compound_effect(self):
        """Test that growth calculation shows compound effect"""
        # With compound growth, longer periods should have higher average growth
        growth_1_year = calculate_growth_over_n_years(0.1, 1)
        growth_5_years = calculate_growth_over_n_years(0.1, 5)
        growth_10_years = calculate_growth_over_n_years(0.1, 10)
        
        self.assertLess(growth_1_year, growth_5_years)
        self.assertLess(growth_5_years, growth_10_years)

    def test_calculate_growth_mathematical_correctness(self):
        """Test mathematical correctness of growth calculation"""
        # For 10% yield over 3 years:
        # Year 1: 1.1, Year 2: 1.21, Year 3: 1.331
        # Average: (1.1 + 1.21 + 1.331) / 3 = 2.641 / 3 = 0.880333...
        growth = calculate_growth_over_n_years(0.1, 3)
        expected = (1.1 + 1.21 + 1.331) / 3
        self.assertAlmostEqual(growth, expected, places=6)

    def test_calculate_monthly_required_basic(self):
        """Test basic monthly required calculation"""
        # If you want 12000 in 1 year with no growth (g=1), 
        # you need 12000 / (1 * 12 * 1) = 1000 per month
        monthly = calculate_monthly_required_to_reach_z(12000, 1, 1.0)
        self.assertEqual(monthly, 1000.0)

    def test_calculate_monthly_required_with_growth(self):
        """Test monthly required calculation with growth"""
        # With growth factor of 1.5, you need less monthly investment
        monthly_no_growth = calculate_monthly_required_to_reach_z(12000, 1, 1.0)
        monthly_with_growth = calculate_monthly_required_to_reach_z(12000, 1, 1.5)
        
        self.assertLess(monthly_with_growth, monthly_no_growth)
        self.assertAlmostEqual(monthly_with_growth, 12000 / (1.5 * 12 * 1), places=6)

    def test_calculate_monthly_required_longer_period(self):
        """Test monthly required calculation over longer periods"""
        # Longer investment periods should require less monthly investment
        monthly_1_year = calculate_monthly_required_to_reach_z(24000, 1, 1.2)
        monthly_2_years = calculate_monthly_required_to_reach_z(24000, 2, 1.2)
        
        self.assertLess(monthly_2_years, monthly_1_year)

    def test_calculate_monthly_required_zero_target(self):
        """Test monthly required calculation with zero target"""
        monthly = calculate_monthly_required_to_reach_z(0, 5, 1.5)
        self.assertEqual(monthly, 0.0)

    def test_calculate_monthly_required_realistic_scenario(self):
        """Test monthly required calculation with realistic values"""
        # Want €100,000 in 10 years with 7% annual yield
        # First calculate realistic growth factor
        growth = calculate_growth_over_n_years(0.07, 10)
        monthly = calculate_monthly_required_to_reach_z(100000, 10, growth)
        
        # Should be a reasonable monthly amount (less than target/months)
        self.assertGreater(monthly, 0)
        self.assertLess(monthly, 100000 / (12 * 10))  # Less than if no growth

    def test_edge_cases_small_values(self):
        """Test edge cases with very small values"""
        # Small yield
        growth = calculate_growth_over_n_years(0.001, 5)
        self.assertGreater(growth, 1.0)
        self.assertLess(growth, 1.1)  # Should be close to 1 for small yield

    def test_edge_cases_large_values(self):
        """Test edge cases with large values"""
        # Large target amount
        monthly = calculate_monthly_required_to_reach_z(1000000, 20, 2.0)
        self.assertGreater(monthly, 0)
        
        # Large number of years
        growth = calculate_growth_over_n_years(0.05, 50)
        self.assertGreater(growth, 1.0)

    def test_mathematical_relationships(self):
        """Test mathematical relationships between functions"""
        # If you invest the calculated monthly amount, you should reach your target
        target = 50000
        years = 5
        yield_rate = 0.08
        
        growth = calculate_growth_over_n_years(yield_rate, years)
        monthly = calculate_monthly_required_to_reach_z(target, years, growth)
        total_invested = calculate_principal(monthly * 12, years)
        total_with_growth = total_invested * growth
        
        # The total with growth should approximately equal the target
        self.assertAlmostEqual(total_with_growth, target, delta=1.0)


if __name__ == '__main__':
    unittest.main()
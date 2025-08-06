import unittest
import sys
import os

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from constants import interest_rates, INTEREST_DEDUCTION


class TestConstants(unittest.TestCase):
    """Test cases for constants.py"""

    def test_interest_deduction_exists(self):
        """Test that INTEREST_DEDUCTION constant exists and is reasonable"""
        self.assertIsInstance(INTEREST_DEDUCTION, (int, float))
        self.assertGreater(INTEREST_DEDUCTION, 0)
        self.assertLess(INTEREST_DEDUCTION, 100)  # Should be a percentage less than 100%

    def test_interest_rates_structure(self):
        """Test that interest_rates has the expected structure"""
        # Check that all expected year keys exist
        expected_year_keys = ["Variable", "5", "10", "15", "20", "30"]
        for year_key in expected_year_keys:
            self.assertIn(year_key, interest_rates, f"Missing year key: {year_key}")

        # Check that all expected portion keys exist for each year
        expected_portion_keys = ["NHG", "≤65%", "≤85%", "≤90%", ">90%"]
        for year_key in expected_year_keys:
            for portion_key in expected_portion_keys:
                self.assertIn(portion_key, interest_rates[year_key], 
                            f"Missing portion key {portion_key} for year {year_key}")

    def test_interest_rates_are_positive(self):
        """Test that all interest rates are positive numbers"""
        for year_key, year_data in interest_rates.items():
            for portion_key, rate in year_data.items():
                self.assertIsInstance(rate, (int, float), 
                                    f"Rate for {year_key}/{portion_key} is not a number")
                self.assertGreater(rate, 0, 
                                 f"Rate for {year_key}/{portion_key} should be positive")

    def test_interest_rates_reasonable_range(self):
        """Test that interest rates are in a reasonable range"""
        for year_key, year_data in interest_rates.items():
            for portion_key, rate in year_data.items():
                # Interest rates should typically be between 0.1% and 15%
                self.assertGreaterEqual(rate, 0.1, 
                                      f"Rate {rate} for {year_key}/{portion_key} seems too low")
                self.assertLessEqual(rate, 15.0, 
                                   f"Rate {rate} for {year_key}/{portion_key} seems too high")

    def test_interest_rates_risk_premium_logic(self):
        """Test that higher risk (higher LTV) generally means higher rates"""
        portion_keys_ordered = ["NHG", "≤65%", "≤85%", "≤90%", ">90%"]
        
        for year_key in interest_rates.keys():
            rates = [interest_rates[year_key][portion_key] for portion_key in portion_keys_ordered]
            
            # NHG should generally have the lowest rate (or close to it)
            nhg_rate = rates[0]
            # >90% should generally have the highest rate
            highest_ltv_rate = rates[-1]
            
            # The highest LTV should have a rate >= NHG rate (risk premium)
            self.assertGreaterEqual(highest_ltv_rate, nhg_rate, 
                                  f"Risk premium logic failed for {year_key}: "
                                  f">90% rate ({highest_ltv_rate}) should be >= NHG rate ({nhg_rate})")

    def test_interest_rates_maturity_logic(self):
        """Test that longer-term rates follow reasonable patterns"""
        # Get Variable rate as baseline for short-term
        variable_rates = interest_rates["Variable"]
        
        # Compare with 30-year rates
        thirty_year_rates = interest_rates["30"]
        
        for portion_key in variable_rates.keys():
            variable_rate = variable_rates[portion_key]
            thirty_year_rate = thirty_year_rates[portion_key]
            
            # Typically, longer-term rates can be higher or lower than short-term
            # but should be in a reasonable relationship (within ~3 percentage points)
            rate_difference = abs(thirty_year_rate - variable_rate)
            self.assertLessEqual(rate_difference, 3.0, 
                               f"Rate difference too large between Variable and 30-year for {portion_key}: "
                               f"Variable={variable_rate}, 30-year={thirty_year_rate}")

    def test_specific_rate_values_exist(self):
        """Test that specific combinations of rates exist and are accessible"""
        # Test some specific scenarios that should exist
        test_cases = [
            ("Variable", "NHG"),
            ("5", "≤65%"),
            ("30", ">90%"),
            ("10", "≤85%")
        ]
        
        for year_key, portion_key in test_cases:
            rate = interest_rates[year_key][portion_key]
            self.assertIsInstance(rate, (int, float))
            self.assertGreater(rate, 0)

    def test_interest_rates_precision(self):
        """Test that interest rates have reasonable precision"""
        for year_key, year_data in interest_rates.items():
            for portion_key, rate in year_data.items():
                # Rates should typically have at most 2 decimal places for practical use
                # Allow for floating point precision issues by checking if round to 2 places equals itself
                rounded_rate = round(rate, 2)
                self.assertAlmostEqual(rate, rounded_rate, places=3,
                                     msg=f"Rate {rate} for {year_key}/{portion_key} has too many decimal places")

    def test_constants_immutability_concept(self):
        """Test that constants maintain their expected values (basic sanity check)"""
        # Basic test to ensure the constants haven't been accidentally modified
        self.assertIsNotNone(interest_rates)
        self.assertIsInstance(interest_rates, dict)
        self.assertGreater(len(interest_rates), 0)
        
        self.assertIsNotNone(INTEREST_DEDUCTION)
        self.assertIsInstance(INTEREST_DEDUCTION, (int, float))

    def test_nhg_rates_competitive(self):
        """Test that NHG rates are competitive (generally lower or equal to other rates)"""
        for year_key in interest_rates.keys():
            nhg_rate = interest_rates[year_key]["NHG"]
            year_rates = list(interest_rates[year_key].values())
            min_rate = min(year_rates)
            
            # NHG rate should be among the lower rates (within 0.5 percentage points of minimum)
            self.assertLessEqual(nhg_rate - min_rate, 0.5, 
                               f"NHG rate for {year_key} is not competitive: "
                               f"NHG={nhg_rate}, min={min_rate}")

    def test_data_completeness(self):
        """Test that the interest rates data is complete"""
        # Count total entries
        total_entries = sum(len(year_data) for year_data in interest_rates.values())
        expected_entries = 6 * 5  # 6 year categories × 5 portion categories
        
        self.assertEqual(total_entries, expected_entries, 
                        "Interest rates data appears to be incomplete")


if __name__ == '__main__':
    unittest.main()
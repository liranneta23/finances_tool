import unittest
import sys
import os

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gifts import (
    calculate_gift_tax, 
    gift_tax_net,
    HOME_ACQUISITION_EXEMPTION,
    ANNUAL_PARENTAL_EXEMPTION,
    FIRST_BRACKET_LIMIT,
    FIRST_BRACKET_RATE,
    SECOND_BRACKET_RATE
)


class TestGifts(unittest.TestCase):
    """Test cases for gifts.py"""

    def test_calculate_gift_tax_no_tax(self):
        """Test gift tax calculation when no tax is due"""
        total_exemption = HOME_ACQUISITION_EXEMPTION + ANNUAL_PARENTAL_EXEMPTION
        
        # Gift amount exactly equal to exemptions
        self.assertEqual(calculate_gift_tax(total_exemption), 0.0)
        
        # Gift amount less than exemptions
        self.assertEqual(calculate_gift_tax(total_exemption - 1000), 0.0)
        self.assertEqual(calculate_gift_tax(50000), 0.0)

    def test_calculate_gift_tax_first_bracket(self):
        """Test gift tax calculation in the first tax bracket"""
        total_exemption = HOME_ACQUISITION_EXEMPTION + ANNUAL_PARENTAL_EXEMPTION
        
        # Small amount in first bracket
        gift_amount = total_exemption + 10000
        expected_tax = 10000 * FIRST_BRACKET_RATE
        self.assertEqual(calculate_gift_tax(gift_amount), expected_tax)
        
        # Larger amount still in first bracket
        gift_amount = total_exemption + 50000
        expected_tax = 50000 * FIRST_BRACKET_RATE
        self.assertEqual(calculate_gift_tax(gift_amount), expected_tax)

    def test_calculate_gift_tax_second_bracket(self):
        """Test gift tax calculation in the second tax bracket"""
        total_exemption = HOME_ACQUISITION_EXEMPTION + ANNUAL_PARENTAL_EXEMPTION
        
        # Amount that reaches second bracket
        gift_amount = total_exemption + FIRST_BRACKET_LIMIT + 20000
        expected_tax = (FIRST_BRACKET_LIMIT * FIRST_BRACKET_RATE) + (20000 * SECOND_BRACKET_RATE)
        self.assertEqual(calculate_gift_tax(gift_amount), expected_tax)

    def test_calculate_gift_tax_exact_bracket_boundary(self):
        """Test gift tax calculation at the exact bracket boundary"""
        total_exemption = HOME_ACQUISITION_EXEMPTION + ANNUAL_PARENTAL_EXEMPTION
        
        # Amount exactly at the first bracket limit
        gift_amount = total_exemption + FIRST_BRACKET_LIMIT
        expected_tax = FIRST_BRACKET_LIMIT * FIRST_BRACKET_RATE
        self.assertEqual(calculate_gift_tax(gift_amount), expected_tax)

    def test_gift_tax_net_no_tax(self):
        """Test gift_tax_net function when no tax is due"""
        gift_amount = 100000
        tax, net = gift_tax_net(gift_amount)
        
        self.assertEqual(tax, 0.0)
        self.assertEqual(net, gift_amount)

    def test_gift_tax_net_with_tax(self):
        """Test gift_tax_net function when tax is due"""
        total_exemption = HOME_ACQUISITION_EXEMPTION + ANNUAL_PARENTAL_EXEMPTION
        gift_amount = total_exemption + 50000
        
        tax, net = gift_tax_net(gift_amount)
        expected_tax = 50000 * FIRST_BRACKET_RATE
        expected_net = gift_amount - expected_tax
        
        self.assertEqual(tax, expected_tax)
        self.assertEqual(net, expected_net)

    def test_gift_tax_constants(self):
        """Test that gift tax constants are reasonable values"""
        # Check that exemptions are positive
        self.assertGreater(HOME_ACQUISITION_EXEMPTION, 0)
        self.assertGreater(ANNUAL_PARENTAL_EXEMPTION, 0)
        
        # Check that bracket limit is positive
        self.assertGreater(FIRST_BRACKET_LIMIT, 0)
        
        # Check that tax rates are between 0 and 1
        self.assertTrue(0 <= FIRST_BRACKET_RATE <= 1)
        self.assertTrue(0 <= SECOND_BRACKET_RATE <= 1)
        
        # Check that second bracket rate is higher than first
        self.assertGreater(SECOND_BRACKET_RATE, FIRST_BRACKET_RATE)

    def test_large_gift_amounts(self):
        """Test gift tax calculation with very large amounts"""
        large_amount = 1000000  # 1 million
        tax = calculate_gift_tax(large_amount)
        
        # Tax should be positive for large amounts
        self.assertGreater(tax, 0)
        
        # Tax should be less than the gift amount
        self.assertLess(tax, large_amount)

    def test_zero_gift_amount(self):
        """Test gift tax calculation with zero gift amount"""
        self.assertEqual(calculate_gift_tax(0), 0.0)
        
        tax, net = gift_tax_net(0)
        self.assertEqual(tax, 0.0)
        self.assertEqual(net, 0.0)


if __name__ == '__main__':
    unittest.main()
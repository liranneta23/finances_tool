import unittest
from unittest.mock import patch
from io import StringIO

# Import the functions to test
from gifts import (
    calculate_gift_tax,
    gift_tax_net,
    gift_calculations,
    HOME_ACQUISITION_EXEMPTION,
    ANNUAL_PARENTAL_EXEMPTION,
    FIRST_BRACKET_LIMIT,
    FIRST_BRACKET_RATE,
    SECOND_BRACKET_RATE
)


class TestGifts(unittest.TestCase):
    
    def test_calculate_gift_tax_below_exemption(self):
        """Test gift tax calculation when amount is below total exemptions"""
        # Total exemptions = 114318 + 6035 = 120353
        total_exemptions = HOME_ACQUISITION_EXEMPTION + ANNUAL_PARENTAL_EXEMPTION
        
        # Test with amount below exemptions
        tax = calculate_gift_tax(50000)
        self.assertEqual(tax, 0)
        
        # Test with amount equal to exemptions
        tax = calculate_gift_tax(total_exemptions)
        self.assertEqual(tax, 0)
        
    def test_calculate_gift_tax_first_bracket(self):
        """Test gift tax calculation in first bracket (10%)"""
        total_exemptions = HOME_ACQUISITION_EXEMPTION + ANNUAL_PARENTAL_EXEMPTION
        
        # Test with amount just above exemptions
        taxable_amount = 10000
        gift_amount = total_exemptions + taxable_amount
        expected_tax = taxable_amount * FIRST_BRACKET_RATE
        tax = calculate_gift_tax(gift_amount)
        self.assertEqual(tax, expected_tax)
        
        # Test with amount at first bracket limit
        gift_amount = total_exemptions + FIRST_BRACKET_LIMIT
        expected_tax = FIRST_BRACKET_LIMIT * FIRST_BRACKET_RATE
        tax = calculate_gift_tax(gift_amount)
        self.assertEqual(tax, expected_tax)
        
    def test_calculate_gift_tax_second_bracket(self):
        """Test gift tax calculation in second bracket (20%)"""
        total_exemptions = HOME_ACQUISITION_EXEMPTION + ANNUAL_PARENTAL_EXEMPTION
        
        # Test with amount above first bracket limit
        amount_above_limit = 50000
        gift_amount = total_exemptions + FIRST_BRACKET_LIMIT + amount_above_limit
        expected_tax = (FIRST_BRACKET_LIMIT * FIRST_BRACKET_RATE) + (amount_above_limit * SECOND_BRACKET_RATE)
        tax = calculate_gift_tax(gift_amount)
        self.assertEqual(tax, expected_tax)
        
    def test_gift_tax_net(self):
        """Test gift_tax_net function"""
        gift_amount = 200000
        tax, net = gift_tax_net(gift_amount)
        
        # Verify tax calculation
        expected_tax = calculate_gift_tax(gift_amount)
        self.assertEqual(tax, expected_tax)
        
        # Verify net calculation
        expected_net = gift_amount - expected_tax
        self.assertEqual(net, expected_net)
        
        # Test with zero amount
        tax, net = gift_tax_net(0)
        self.assertEqual(tax, 0)
        self.assertEqual(net, 0)
        
    @patch('builtins.input', return_value='150000')
    @patch('sys.stdout', new_callable=StringIO)
    def test_gift_calculations(self, mock_stdout, mock_input):
        """Test gift_calculations function with mocked input"""
        gift_calculations()
        output = mock_stdout.getvalue()
        
        # Check that the output contains expected information
        self.assertIn("Gift Amount: €150000.00", output)
        self.assertIn("Estimated Gift Tax: €", output)
        self.assertIn("Net Amount After Tax: €", output)
        
    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Test with very small amount
        tax = calculate_gift_tax(0.01)
        self.assertEqual(tax, 0)
        
        # Test with very large amount
        large_amount = 1000000
        tax = calculate_gift_tax(large_amount)
        self.assertGreater(tax, 0)
        
        # Test exact boundary between brackets
        total_exemptions = HOME_ACQUISITION_EXEMPTION + ANNUAL_PARENTAL_EXEMPTION
        boundary_amount = total_exemptions + FIRST_BRACKET_LIMIT
        tax = calculate_gift_tax(boundary_amount)
        expected_tax = FIRST_BRACKET_LIMIT * FIRST_BRACKET_RATE
        self.assertEqual(tax, expected_tax)
        
    def test_constants(self):
        """Test that constants are correctly defined"""
        self.assertEqual(HOME_ACQUISITION_EXEMPTION, 114318)
        self.assertEqual(ANNUAL_PARENTAL_EXEMPTION, 6035)
        self.assertEqual(FIRST_BRACKET_LIMIT, 138642)
        self.assertEqual(FIRST_BRACKET_RATE, 0.10)
        self.assertEqual(SECOND_BRACKET_RATE, 0.20)
        
    def test_real_world_examples(self):
        """Test with realistic gift amounts"""
        # Example 1: Small gift
        tax = calculate_gift_tax(50000)
        self.assertEqual(tax, 0)  # Below exemptions
        
        # Example 2: Medium gift
        tax = calculate_gift_tax(150000)
        total_exemptions = HOME_ACQUISITION_EXEMPTION + ANNUAL_PARENTAL_EXEMPTION
        taxable_amount = 150000 - total_exemptions
        expected_tax = taxable_amount * FIRST_BRACKET_RATE
        self.assertEqual(tax, expected_tax)
        
        # Example 3: Large gift
        tax = calculate_gift_tax(300000)
        self.assertGreater(tax, 0)
        # Should be in second bracket


if __name__ == '__main__':
    unittest.main()
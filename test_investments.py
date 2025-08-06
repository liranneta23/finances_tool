import unittest
from unittest.mock import patch
from io import StringIO
import sys

# Import the functions to test
from investments import (
    calculate_principal,
    calculate_growth_over_n_years,
    calculate_monthly_required_to_reach_z,
    total_return,
    find_how_much_to_invest
)


class TestInvestments(unittest.TestCase):
    
    def test_calculate_principal(self):
        """Test calculate_principal function with various inputs"""
        # Test basic calculation
        self.assertEqual(calculate_principal(1000, 5), 5000)
        self.assertEqual(calculate_principal(500, 10), 5000)
        self.assertEqual(calculate_principal(0, 5), 0)
        self.assertEqual(calculate_principal(1000, 0), 0)
        
    def test_calculate_growth_over_n_years(self):
        """Test calculate_growth_over_n_years function with various inputs"""
        # Test with 10% annual yield over 1 year
        result = calculate_growth_over_n_years(0.10, 1)
        self.assertAlmostEqual(result, 1.10, places=2)
        
        # Test with 5% annual yield over 2 years
        result = calculate_growth_over_n_years(0.05, 2)
        expected = ((1.05 ** 1) + (1.05 ** 2)) / 2
        self.assertAlmostEqual(result, expected, places=2)
        
        # Test with 0% yield
        result = calculate_growth_over_n_years(0.0, 5)
        self.assertAlmostEqual(result, 1.0, places=2)
        
    def test_calculate_monthly_required_to_reach_z(self):
        """Test calculate_monthly_required_to_reach_z function"""
        # Test basic calculation
        result = calculate_monthly_required_to_reach_z(10000, 5, 1.5)
        expected = 10000 / (1.5 * 12 * 5)
        self.assertAlmostEqual(result, expected, places=2)
        
        # Test with different parameters
        result = calculate_monthly_required_to_reach_z(50000, 10, 2.0)
        expected = 50000 / (2.0 * 12 * 10)
        self.assertAlmostEqual(result, expected, places=2)
        
    @patch('builtins.input', side_effect=['1000', '10', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_total_return(self, mock_stdout, mock_input):
        """Test total_return function with mocked input"""
        total_return()
        output = mock_stdout.getvalue()
        
        # Check that the output contains expected information
        self.assertIn("The total return after 5 years", output)
        self.assertIn("The total principal after 5 years", output)
        self.assertIn("The total profit after 5 years", output)
        self.assertIn("The total growth in percentage after 5 years", output)
        
    @patch('builtins.input', side_effect=['10000', '8.5', '7'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_how_much_to_invest(self, mock_stdout, mock_input):
        """Test find_how_much_to_invest function with mocked input"""
        find_how_much_to_invest()
        output = mock_stdout.getvalue()
        
        # Check that the output contains expected information
        self.assertIn("You need to invest €", output)
        self.assertIn("every month to reach €10000", output)
        self.assertIn("within 7 years with 8.5% yield", output)
        
    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Test with very small numbers
        self.assertEqual(calculate_principal(0.01, 1), 0.01)
        
        # Test with large numbers
        self.assertEqual(calculate_principal(1000000, 1), 1000000)
        
        # Test growth calculation with very small yield
        result = calculate_growth_over_n_years(0.001, 1)
        self.assertAlmostEqual(result, 1.001, places=3)
        
        # Test monthly calculation with very small desired amount
        result = calculate_monthly_required_to_reach_z(1, 1, 1.1)
        expected = 1 / (1.1 * 12 * 1)
        self.assertAlmostEqual(result, expected, places=6)


if __name__ == '__main__':
    unittest.main()
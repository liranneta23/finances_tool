import unittest
import sys
import os

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from helper_functions import decimal_to_percentage


class TestHelperFunctions(unittest.TestCase):
    """Test cases for helper_functions.py"""

    def test_decimal_to_percentage_basic(self):
        """Test basic decimal to percentage conversion"""
        self.assertEqual(decimal_to_percentage(1.0), 0.0)
        self.assertEqual(decimal_to_percentage(1.1), 10.0)
        self.assertEqual(decimal_to_percentage(1.5), 50.0)
        self.assertEqual(decimal_to_percentage(2.0), 100.0)

    def test_decimal_to_percentage_precision(self):
        """Test decimal to percentage conversion with precision"""
        self.assertEqual(decimal_to_percentage(1.123), 12.3)
        self.assertEqual(decimal_to_percentage(1.127), 12.7)
        self.assertEqual(decimal_to_percentage(1.1249), 12.5)  # Tests rounding

    def test_decimal_to_percentage_edge_cases(self):
        """Test edge cases for decimal to percentage conversion"""
        self.assertEqual(decimal_to_percentage(0.9), -10.0)  # Negative percentage
        self.assertEqual(decimal_to_percentage(1.001), 0.1)   # Small positive
        self.assertEqual(decimal_to_percentage(0.999), -0.1)  # Small negative

    def test_decimal_to_percentage_large_values(self):
        """Test decimal to percentage conversion with large values"""
        self.assertEqual(decimal_to_percentage(5.0), 400.0)
        self.assertEqual(decimal_to_percentage(10.0), 900.0)


if __name__ == '__main__':
    unittest.main()
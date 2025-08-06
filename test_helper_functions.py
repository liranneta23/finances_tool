import unittest

# Import the function to test
from helper_functions import decimal_to_percentage


class TestHelperFunctions(unittest.TestCase):
    
    def test_decimal_to_percentage_basic(self):
        """Test decimal_to_percentage function with basic inputs"""
        # Test with 1.0 (no growth)
        result = decimal_to_percentage(1.0)
        self.assertEqual(result, 0.0)
        
        # Test with 1.1 (10% growth)
        result = decimal_to_percentage(1.1)
        self.assertEqual(result, 10.0)
        
        # Test with 1.05 (5% growth)
        result = decimal_to_percentage(1.05)
        self.assertEqual(result, 5.0)
        
        # Test with 2.0 (100% growth)
        result = decimal_to_percentage(2.0)
        self.assertEqual(result, 100.0)
        
    def test_decimal_to_percentage_decimal_places(self):
        """Test decimal_to_percentage function with decimal precision"""
        # Test with 1.123 (12.3% growth)
        result = decimal_to_percentage(1.123)
        self.assertEqual(result, 12.3)
        
        # Test with 1.567 (56.7% growth)
        result = decimal_to_percentage(1.567)
        self.assertEqual(result, 56.7)
        
        # Test with 1.001 (0.1% growth)
        result = decimal_to_percentage(1.001)
        self.assertEqual(result, 0.1)
        
    def test_decimal_to_percentage_edge_cases(self):
        """Test decimal_to_percentage function with edge cases"""
        # Test with 0.5 (negative growth)
        result = decimal_to_percentage(0.5)
        self.assertEqual(result, -50.0)
        
        # Test with 0.9 (negative growth)
        result = decimal_to_percentage(0.9)
        self.assertEqual(result, -10.0)
        
        # Test with 0.0 (complete loss)
        result = decimal_to_percentage(0.0)
        self.assertEqual(result, -100.0)
        
    def test_decimal_to_percentage_rounding(self):
        """Test that decimal_to_percentage rounds to 1 decimal place"""
        # Test with 1.123456 (should round to 12.3)
        result = decimal_to_percentage(1.123456)
        self.assertEqual(result, 12.3)
        
        # Test with 1.999999 (should round to 100.0)
        result = decimal_to_percentage(1.999999)
        self.assertEqual(result, 100.0)
        
        # Test with 1.000001 (should round to 0.0)
        result = decimal_to_percentage(1.000001)
        self.assertEqual(result, 0.0)
        
    def test_decimal_to_percentage_real_world_examples(self):
        """Test with realistic investment growth scenarios"""
        # 7% annual return
        result = decimal_to_percentage(1.07)
        self.assertEqual(result, 7.0)
        
        # 15% annual return
        result = decimal_to_percentage(1.15)
        self.assertEqual(result, 15.0)
        
        # 3.5% annual return
        result = decimal_to_percentage(1.035)
        self.assertEqual(result, 3.5)
        
        # -5% annual return (loss)
        result = decimal_to_percentage(0.95)
        self.assertEqual(result, -5.0)


if __name__ == '__main__':
    unittest.main()
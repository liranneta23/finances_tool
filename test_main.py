import unittest
from unittest.mock import patch
from io import StringIO
import sys

# Import the function to test
from main import main


class TestMain(unittest.TestCase):
    
    @patch('builtins.input', side_effect=['1', '1000', '10', '5', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_option_1(self, mock_stdout, mock_input):
        """Test main function with menu option 1 (total return)"""
        # Since main() has an infinite loop, we'll test it differently
        # Let's test the menu display by calling main() and checking the first iteration
        try:
            main()
        except StopIteration:
            pass  # Expected when mock input runs out
        
        output = mock_stdout.getvalue()
        
        # Check that the menu displays
        self.assertIn("*** Menu ***", output)
        self.assertIn("1. Calculate return given annual principal, annual yield and number of years", output)
        self.assertIn("2. Calculate the required monthly invested to reach your desired amount", output)
        self.assertIn("3. Gift calculations", output)
        self.assertIn("4. Mortgage calculations", output)
        
    @patch('builtins.input', side_effect=['2', '10000', '8.5', '7', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_option_2(self, mock_stdout, mock_input):
        """Test main function with menu option 2 (find how much to invest)"""
        try:
            main()
        except StopIteration:
            pass
        
        output = mock_stdout.getvalue()
        
        # Check that the menu displays and the function executed
        self.assertIn("*** Menu ***", output)
        self.assertIn("You need to invest €", output)
        
    @patch('builtins.input', side_effect=['3', '150000', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_option_3(self, mock_stdout, mock_input):
        """Test main function with menu option 3 (gift calculations)"""
        try:
            main()
        except StopIteration:
            pass
        
        output = mock_stdout.getvalue()
        
        # Check that the menu displays and the function executed
        self.assertIn("*** Menu ***", output)
        self.assertIn("Gift Amount: €150000.00", output)
        
    @patch('builtins.input', side_effect=['4', '200000', '5', '10', '1', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_option_4(self, mock_stdout, mock_input):
        """Test main function with menu option 4 (mortgage calculations)"""
        try:
            main()
        except StopIteration:
            pass
        
        output = mock_stdout.getvalue()
        
        # Check that the menu displays and the function executed
        self.assertIn("*** Menu ***", output)
        self.assertIn("*** Calculate your mortgage***", output)
        
    @patch('builtins.input', side_effect=['5', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_invalid_choice(self, mock_stdout, mock_input):
        """Test main function with invalid menu choice"""
        try:
            main()
        except StopIteration:
            pass
        
        output = mock_stdout.getvalue()
        
        # Check that invalid choice message is displayed
        self.assertIn("Invalid choice. Please enter 1 or 2.", output)
        
    @patch('builtins.input', side_effect=['abc', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_non_numeric_input(self, mock_stdout, mock_input):
        """Test main function with non-numeric input"""
        try:
            main()
        except StopIteration:
            pass
        
        output = mock_stdout.getvalue()
        
        # Check that invalid choice message is displayed
        self.assertIn("Invalid choice. Please enter 1 or 2.", output)
        
    def test_choices_dictionary_structure(self):
        """Test that the choices dictionary is properly structured"""
        # Since choices_dictionary is defined inside main(), we need to test it differently
        # Let's test that the functions exist and are callable
        from investments import total_return, find_how_much_to_invest
        from gifts import gift_calculations
        from mortgage import mortgage
        
        # Check that all functions are callable
        self.assertTrue(callable(total_return))
        self.assertTrue(callable(find_how_much_to_invest))
        self.assertTrue(callable(gift_calculations))
        self.assertTrue(callable(mortgage))


if __name__ == '__main__':
    unittest.main()
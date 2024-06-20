import pytest
from  is_palindrome import is_palindrome

#The @pytest.mark.parametrize decorator in pytest allows you
# to run a test function multiple times with different sets of arguments. 
# This is useful for testing a function with a variety of input values
# to ensure it behaves correctly under different conditions.

# test_palindrome.py
import pytest
from is_palindrome import is_palindrome

@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("A man, a plan, a canal, Panama", True),  # Palindrome with punctuation and spaces
        ("racecar", True),                         # Simple palindrome
        ("Hello, World!", False),                  # Not a palindrome
        ("", True),                                # Empty string is a palindrome
        ("No 'x' in Nixon", True),                 # Palindrome with punctuation
        ("abc", False),
        ("abab", False),
    ]
)
def test_is_palindrome(test_input, expected):
    assert is_palindrome(test_input) == expected

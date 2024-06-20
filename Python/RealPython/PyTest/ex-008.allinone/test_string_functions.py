import pytest

from string_functions import (
    capitalize,
    lowercase,
    uppercase,
    is_palindrome,
    is_blank,
    replace,
    split,
    join,
    count_occurrences,
    strip_whitespace,
)


@pytest.mark.parametrize(
    "text, expected_output",
    [
        ("hello", "Hello"),
        ("WORLD", "World"),
    ],
)
def test_capitalize(text, expected_output):
    """Tests the capitalize function with different inputs."""
    assert capitalize(text) == expected_output


@pytest.mark.parametrize(
    "text",
    [
        "Hello, world!",
        "This IS a MiXeD cAsE string.",
    ],
)
def test_lowercase(text):
    """Tests the lowercase function with different inputs."""
    assert lowercase(text) == text.lower()

@pytest.mark.parametrize(
    "text, expected_output",
    [
        ("hello", "HELLO"),
        ("WORLD", "WORLD"),
    ],
)
def test_uppercase(text, expected_output):
    """Tests the upper function with different inputs."""
    assert uppercase(text) == text.upper()


@pytest.mark.parametrize(
    "text, expected_output",
    [
        ("racecar", True),
        ("hello", False),
    ],
)
def test_is_palindrome(text, expected_output):
    """Tests if is a palindrome string."""
    assert is_palindrome(text) == expected_output

@pytest.mark.parametrize(
    "text, expected_output",
    [
        ("", True),
        ("hello", False),
    ],
)
def test_is_blank(text, expected_output):
    """Tests if is a palindrome string."""
    assert is_blank(text) == expected_output

@pytest.mark.parametrize(
    "text, old, new, expected_output",
    [
        ("Hello World", "Hello", "Hi", "Hi World"),
        ("Hello World", "World", "Earth", "Hello Earth"),
        ("HelloWorld", "World", "Earth", "HelloEarth"),  # No space between words
        ("banana", "a", "A", "bAnAnA"),  # Multiple occurrences replaced
    ],
)
def test_replace(text, old, new, expected_output ):
  """Test string replacement"""
  assert text.replace(old, new) == expected_output
  
@pytest.mark.parametrize(
    "text, separator, expected_output",
    [
        ("Hello,world", ",", ["Hello", "world"]),
        ("This is a string", " ", ["This", "is", "a", "string"]),
        ("banana,split", ",", ["banana", "split"]),  # Test with empty elements
        ("", ",", [""]),  # Test empty string
        ("noseparator", "", ['noseparator']),  # Test missing separator
    ],
)
def test_split(text, separator, expected_output):
    """Tests string splitting with various inputs."""
    if separator == "":
        with pytest.raises(ValueError) as excinfo:
            split(text, separator)
        assert str(excinfo.value) == "empty separator"
    else:
        assert split(text, separator) == expected_output

@pytest.mark.parametrize(
    "text_list, separator, expected_output",
    [
        (["Hello", "world"], ", ", "Hello, world"),
        (["This", "is", "a", "string"], " ", "This is a string"),
        ([], ",", ""),  # Test empty list
    ],
)
def test_join(text_list, separator, expected_output):
    """Tests string joining with various inputs."""
    assert join(text_list, separator) == expected_output

@pytest.mark.parametrize(
    "text, char, expected_count",
    [
        ("hello world", "l", 3),
        ("Mississippi", "s", 4),
        ("banana", "a", 3),  # Test multiple occurrences
        ("", "x", 0),  # Test empty string
    ],
)
def test_count_occurrences(text, char, expected_count):
    """Tests counting occurrences of a character in a string."""
    assert count_occurrences(text, char) == expected_count

@pytest.mark.parametrize(
    "text, expected_output",
    [
        ("  Hello world  ", "Hello world"),
        ("\tThis\n is a string\r", "This\n is a string"),
        ("", ""),  # Test empty string
        ("   ", ""),  # Test only whitespace
    ],
)
def test_strip_whitespace(text, expected_output):
    """Tests whitespace removal from a string."""
    assert strip_whitespace(text) == expected_output
    
    
# Use data from conftest.py fixture
def test_capitalize_sample_data(sample_data):
  """Tests capitalize using sample data from the fixture."""
  assert capitalize(sample_data["name"]) == "John doe"
  
  
@pytest.mark.slow
def test_slow_function():
  # Perform a time-consuming operation
    for _ in range(1000000):
        pass
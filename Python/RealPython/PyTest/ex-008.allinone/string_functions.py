
def capitalize(text):
  """Capitalizes the first letter of a string."""
  return text.capitalize()

def lowercase(text):
  """Converts a string to lowercase."""
  return text.lower()

def uppercase(text):
  """Converts a string to uppercase."""
  return text.upper()

def is_palindrome(text):
  """Checks if a string is a palindrome."""
  return text.lower() == text.lower()[::-1]

def is_blank(text):
  """Checks if a string is empty or consists only of whitespace."""
  return not text.strip()

def replace(text, old, new):
  """Replaces all occurrences of 'old' with 'new' in a string."""
  return text.replace(old, new)

def split(text, separator):
  """Splits a string based on a given separator."""
  return text.split(separator)

def join(text_list, separator):
  """Joins a list of strings with a separator."""
  return separator.join(text_list)

def count_occurrences(text, char):
  """Counts the occurrences of a character in a string."""
  return text.count(char)

def strip_whitespace(text):
  """Removes leading, trailing, and internal whitespace from a string."""
  return text.strip()



def is_palindrome(s):
    """
    Checks if a given string is a palindrome.
    
    Args:
        s (str): The string to check.
        
    Returns:
        bool: True if the string is a palindrome, False otherwise.
    """
    # Normalize the string by converting it to lowercase and removing non-alphanumeric characters
    normalized_str = ''.join(char.lower() for char in s if char.isalnum())
    # Check if the normalized string is equal to its reverse
    return normalized_str == normalized_str[::-1]
import requests

def get_data(url):
  """
  Makes a GET request to the specified URL and returns the response content.

  Args:
      url: The URL to send the GET request to.

  Returns:
      The response content as a string (if successful) or None (if an error occurs).

  Raises:
      RuntimeError: If network calls are disabled (due to the `disable_network_calls` fixture).
  """
  if not requests.get:  # Check if network calls are disabled
    raise RuntimeError("Network access is disabled during testing!")

  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for non-200 status codes
    return response.text  # Assuming the response content is text
  except requests.exceptions.RequestException as e:
    print(f"Error making request to {url}: {e}")
    return None  # Or handle the error differently
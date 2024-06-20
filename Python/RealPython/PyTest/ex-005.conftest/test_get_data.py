# Assuming the function is in a file called 'get_data.py'
import pytest

from get_data import get_data

def test_get_data_disabled_network():
  """
  Tests that get_data raises an error when network calls are disabled.
  """
  with pytest.raises(RuntimeError) as excinfo:
    get_data("https://www.example.com")
  assert str(excinfo.value) == "Network access not allowed during testing!"

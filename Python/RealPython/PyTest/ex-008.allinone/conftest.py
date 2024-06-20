# This conftest.py defines a fixture named sample_data that returns a dictionary containing sample data.
# This data can be used across your test files without the need to define it repeatedly.

import pytest

@pytest.fixture
def sample_data():
  """Provides sample data for various tests."""
  return {
      "name": "John Doe",
      "age": 30,
      "city": "New York",
  }

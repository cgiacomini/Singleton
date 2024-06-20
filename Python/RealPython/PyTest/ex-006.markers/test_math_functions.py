import pytest

from math_functions import add, subtract

@pytest.mark.basic  # Marker for basic functionality tests
def test_add():
  assert add(2, 3) == 5

@pytest.mark.basic
def test_subtract():
  assert subtract(7, 4) == 3


@pytest.mark.advanced  # Marker for more complex tests (optional)
def test_add_large_numbers():
  assert add(1e6, 2e6) == 3e6  # Example of a complex test

@pytest.mark.skip  # Skips this test by default (can be run explicitly)
def test_division_by_zero():
  with pytest.raises(ZeroDivisionError):
    add(10, 0)


# pytest provides a few marks out of the box:

# skip: skips a test unconditionally.
# skipif:  skips a test if the expression passed to it evaluates to True.
# xfail:  indicates that a test is expected to fail, so if the test does fail, 
#         the overall suite can still result in a passing status.
# parametrize: creates multiple variants of a test with different values 
#         as arguments. You’ll learn more about this mark shortly.
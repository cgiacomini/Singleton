# conftest.py

import pytest
import requests

from get_data import get_data

# if you want to make a fixture available for your whole project without having to import it, 
# a special configuration module called conftest.py will allow you to do that.
# pytest looks for a conftest.py module in each directory starting from 
# the test file's directory and moving up the directory tree.


# The autouse=True parameter tells pytest to automatically use this fixture for all tests.
# @pytest.fixture  This marks the function as a pytest fixture that provides 
# data or modifies test environments.
@pytest.fixture(autouse=True)
def disable_network_calls(monkeypatch):

    # This in called instead of the requests get call
    def stunted_get():
        raise RuntimeError("Network access not allowed during testing!")

    # This line uses the monkeypatch argument to modify the behavior of the get function 
    # from the requests library.
    #  - requests: This specifies the module (requests) whose attribute is being patched.
    #  - get: This is the specific attribute (function) within the requests module being modified.
    #  - lambda *args, **kwargs: stunted_get(): This is a lambda function that acts as 
    #    a replacement for the original get function.
    #  - *args, **kwargs: This part allows the patched function to accept any number 
    #    of arguments and keyword arguments that the original get function might receive.
    #  - stunted_get(): This calls the previously defined stunted_get() function, 
    #    which raises the RuntimeError.
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: stunted_get())
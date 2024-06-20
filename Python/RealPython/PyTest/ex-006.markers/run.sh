
pytest -m advanced
pytest -m basic
pytest -m basic -k test_add
pytest -m advanced -k test_add
pytest --strict-markers

# You can see a list of all the marks that pytest knows about by running pytest --markers.
pytest --markers
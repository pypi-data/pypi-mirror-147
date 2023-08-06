"""
    Dummy conftest.py for kafka_dataclasses.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest
from kafka_dataclasses.core import clear_cache


@pytest.fixture(autouse=True)
def clear_the_cache():
    clear_cache()
    yield
    clear_cache()

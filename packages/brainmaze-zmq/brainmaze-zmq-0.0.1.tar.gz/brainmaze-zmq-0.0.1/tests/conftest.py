
import pytest

from .constants import dummy_constant

@pytest.fixture()
def constant_dummy_fixture():
    print(f"Running dummy_fixture with {dummy_constant}")
    yield dummy_constant
    print("Tearing down dummy_fixture")

@pytest.fixture()
def string_test_dummy_fixture():
    print(f"Running string_test_dummy_fixture")
    yield "This is a constant"
    print("Tearing down string_test_dummy_fixture")
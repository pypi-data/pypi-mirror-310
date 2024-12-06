
from .conftest import constant_dummy_fixture, string_test_dummy_fixture

from .constants import dummy_constant


def test_dummy_constant(constant_dummy_fixture: int):
    print(f"Running test_dummy with {constant_dummy_fixture}")
    assert constant_dummy_fixture == dummy_constant

def test_dummy_string(string_test_dummy_fixture: str):
    test_str = string_test_dummy_fixture
    print(f"Running test_dummy with {test_str}")
    assert test_str == "This is a constant"


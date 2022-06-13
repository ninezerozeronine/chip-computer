import pytest

from sixteen_bit_computer import main

@pytest.mark.parametrize("test_input,expected", [
    (
        "a.asm",
        "a.mc",
    ),
    (
        "foo.asm",
        "foo.mc",
    ),
])
def test_get_mc_filename(test_input, expected):
    assert main.get_mc_filename(test_input) == expected

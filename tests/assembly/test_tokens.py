import pytest

from sixteen_bit_computer.assembly import tokens

@pytest.mark.parametrize("test_input, expected", [
    ("123", True),
    ("-1", True),
    ("0xFF", True),
    ("0o22", True),
    ("0b101", True),
    ("0.45", False),
    ("#", False),
    ("", False),
    ("0q12", False),
    ("0b10#g", False),
    ("blah", False),
])
def test_is_number(test_input, expected):
    assert tokens.is_number(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [
    ("hello", True),
    ("_foobar1", True),
    ("loop_start", True),
    ("42", False),
    ("#0b101", False),
    ("##", False),
    ("", False),
])
def test_is_identifier(test_input, expected):
    assert tokens.is_identifier(test_input) == expected
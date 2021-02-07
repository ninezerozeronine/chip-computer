import pytest

from sixteen_bit_computer import assembly_tokens
from sixteen_bit_computer.assembly_tokens import (
    ALIAS,
    NUMBER,
)


@pytest.mark.parametrize("test_input, expected", [
    ("!_foo", ALIAS),
    ("!NUM_BOXES", ALIAS),
    ("#12", type(None)),
    ("!!hello", type(None)),
    ("NAME", type(None)),
    ("$NAME", type(None)),
])
def test_ALIAS(test_input, expected):
    assert type(ALIAS.from_string(test_input)) == expected


@pytest.mark.parametrize("test_input, expected", [
    ("#123", NUMBER),
    ("#-1", NUMBER),
    ("#0xFF", NUMBER),
    ("#0o22", NUMBER),
    ("#0b101", NUMBER),
    ("#-34", NUMBER),
    ("4", type(None)),
    ("0.45", type(None)),
    ("#", type(None)),
    ("", type(None)),
    ("#0q12", type(None)),
    ("#0b10#g", type(None)),
    ("#blah", type(None)),
])
def test_NUMBER(test_input, expected):
    assert type(NUMBER.from_string(test_input)) == expected





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
    assert assembly_tokens.is_identifier(test_input) == expected

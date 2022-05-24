import pytest

from sixteen_bit_computer import assembly_tokens
from sixteen_bit_computer.assembly_tokens import (
    ANCHOR,
    ALIAS,
    LABEL,
    VARIABLE,
    NUMBER,
    OPCODE,
    MODULE,
    MEMREF,
)
from sixteen_bit_computer.instruction_components import (
    NOOP,
    AND,
)



@pytest.mark.parametrize("test_input, expected", [
    ("@", ANCHOR),
    ("$", type(None)),
    ("&", type(None)),
    ("%", type(None)),
    ("hello", type(None)),
])
def test_ANCHOR(test_input, expected):
    assert type(ANCHOR.from_string(test_input)) == expected


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
    ("&hello", LABEL),
    ("&_blah", LABEL),
    ("&MY_MARKER", LABEL),
    ("4", type(None)),
    ("0.45", type(None)),
    ("#", type(None)),
    ("", type(None)),
    ("$012", type(None)),
    ("$//comment", type(None)),
])
def test_LABEL(test_input, expected):
    assert type(LABEL.from_string(test_input)) == expected


@pytest.mark.parametrize("test_input, expected", [
    ("$hello", VARIABLE),
    ("$_blah", VARIABLE),
    ("$MY_VARIABLE", VARIABLE),
    ("4", type(None)),
    ("0.45", type(None)),
    ("#", type(None)),
    ("", type(None)),
    ("$012", type(None)),
    ("$//comment", type(None)),
])
def test_VARIABLE(test_input, expected):
    assert type(VARIABLE.from_string(test_input)) == expected


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


@pytest.mark.parametrize("test_input, expected_token, expected_component", [
    ("NOOP", OPCODE, NOOP),
    ("AND", OPCODE, AND),
    ("FOO", type(None), None),
    ("ANDZZ", type(None), None),
    ("NOOOOP", type(None), None),
    ("#", type(None), None),
    ("", type(None), None),
    ("$012", type(None), None),
    ("$//comment", type(None), None),
])
def test_OPCODE(test_input, expected_token, expected_component):
    res = OPCODE.from_string(test_input)
    assert type(res) == expected_token
    if res is not None:
        assert res.component == expected_component








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

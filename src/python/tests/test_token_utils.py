import pytest

from eight_bit_computer import token_utils

@pytest.mark.parametrize("test_input,expected", [
    ("", False),
    ("      ", False,),
    ("LOAD [$foo] A", False),
    ("@hello", True),
    ("@hello_123_blah", True),
    ("@_my_var", True),
    ("@hello  world  ", False),
    ("@@monkey", False),
    ("@123", False),
])
def test_is_label(test_input, expected):
    assert token_utils.is_label(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    ("", False),
    ("      ", False),
    ("LOAD [$foo] A", False),
    ("$hello", True),
    ("$hello_123_blah", True),
    ("$hello  world  ", False),
    ("$$monkey", False),
    ("$123", False),
])
def test_is_variable(test_input, expected):
    assert token_utils.is_variable(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    ("", False),
    ("      ", False),
    ("LOAD [$foo] A", False),
    ("$hello", True),
    ("#0o22", True),
    ("@blah", True),
    ("A", False),
    ("$$hello", False),
])
def test_is_constant(test_input, expected):
    assert token_utils.is_constant(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    ("#123", True),
    ("#-1", True),
    ("#0xFF", True),
    ("#0o22", True),
    ("#0b101", True),
    ("##", False),
    ("", False),
    ("#0q12", False),
    ("#0b10#g", False),
    ("blah", False),
])
def test_is_number(test_input, expected):
    assert token_utils.is_number(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    (["#123", 123]),
    (["#0", 0]),
    (["#-12", -12]),
    (["#0xFF", 255]),
    (["#0xff", 255]),
    (["#0o10", 8]),
    (["#0b101", 5]),
])
def test_number_constant_value(test_input, expected):
    assert token_utils.number_constant_value(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    ("[A]", True),
    ("[ACC]", True),
    ("[$variable]", True),
    ("[$variable[10]]", True),
    ("[@label]", True),
    ("[#number]", True),
    ("A", False),
    ("$hello", False),
    ("[oops", False),
    ("oops]", False),
    ("$variable[10]", False),
])
def test_is_memory_index(test_input, expected):
    assert token_utils.is_memory_index(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    ("A", "[A]"),
    ("$variable", "[$variable]"),
])
def test_represent_as_memory_index(test_input, expected):
    assert token_utils.represent_as_memory_index(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    ("[A]", "A"),
    ("[ACC]", "ACC"),
    ("[$variable]", "$variable"),
    ("[@label]", "@label"),
    ("[#number]", "#number"),
])
def test_extract_memory_position(test_input, expected):
    assert token_utils.extract_memory_position(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    (
        "",
        [
        ],

    ),
    (
        "    ",
        [
        ],

    ),
    (
        " \t   ",
        [
        ],

    ),
    (
        "hello",
        [
            "hello",
        ],

    ),
    (
        "he./llo world",
        [
            "he./llo",
            "world",
        ],

    ),
    (
        "foo\tbar    baz    ",
        [
            "foo",
            "bar",
            "baz",
        ],

    )
])
def test_get_tokens_from_line(test_input, expected):
    assert token_utils.get_tokens_from_line(test_input) == expected

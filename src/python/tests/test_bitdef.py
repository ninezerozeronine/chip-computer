from contextlib import contextmanager
import pytest

from eight_bit_computer import bitdef


@contextmanager
def does_not_raise():
    yield


@pytest.mark.parametrize("test_input,expected", [
    (
        [
            ".",
            "0",
            "1",
        ],
        True,
    ),
    (
        [
            "...",
            "0.1",
            "1..",
        ],
        True,
    ),
    (
        [
            "",
            "",
        ],
        True,
    ),
    (
        [
            "..",
            "0",
            "1111",
        ],
        False,
    ),
    (
        [
            "...",
            "0.1",
            "1...",
        ],
        False,
    ),
    (
        [
            "...",
            "0.1",
            "",
        ],
        False,
    )
])
def test_same_length(test_input, expected):
    assert bitdef.same_length(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    ("00010", 5),
    ("", 0),
    (".", 1),
    ("01.100", 6),
])
def test_length(test_input, expected):
    assert bitdef.length(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    (
        [
            "0",
            "0",
        ],
        True,
    ),
    (
        [
            "0.",
            "1.",
        ],
        True,
    ),
    (
        [
            "..0.",
            "1.1.",
        ],
        True,
    ),
    (
        [
            "....0.",
            "....1.",
        ],
        True,
    ),
    (
        [
            "......",
            "....0.",
            "....1.",
        ],
        True,
    ),
    (
        [
            "",
        ],
        False,
    ),
    (
        [
            "",
            "",
            "",
        ],
        False,
    ),
    (
        [
            ".",
            "1",
            ".",
        ],
        False,
    ),
    (
        [
            "...0.",
            "1....",
            "..1..",
        ],
        False,
    ),
    (
        [
            "...",
            "...",
            "...",
        ],
        False,
    )
])
def test_have_overlapping_bits(test_input, expected):
    assert bitdef.have_overlapping_bits(test_input) == expected


@pytest.mark.parametrize('test_input', [
    [
        ".10",
        "010.",
    ],
    [
        ".",
        "",
    ],
])
def test_have_overlapping_bits_raises(test_input):
    with pytest.raises(ValueError):
        bitdef.have_overlapping_bits(test_input)

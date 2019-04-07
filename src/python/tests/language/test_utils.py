import pytest

from eight_bit_computer.language import utils

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
    assert utils.get_tokens_from_line(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    (
        [
        ],
        "",
    ),
    (
        [
            "hello",
        ],
        "\"hello\"",
    ),
    (
        [
            "foo",
            "bar",
        ],
        "\"foo\", \"bar\"",
    ),
    (
        [
            "foo",
            "bar",
            "   ",
        ],
        "\"foo\", \"bar\", \"   \"",
    ),
])
def test_add_quotes_to_strings(test_input, expected):
    assert utils.add_quotes_to_strings(test_input) == expected
import pytest

from sixteen_bit_computer import assembler
from sixteen_bit_computer.assembly.tokens import (
    ALIAS,
    NUMBER,
)
from sixteen_bit_computer.assembly.patterns import (
    AliasDefinition,
)
from sixteen_bit_computer.exceptions import (
    NoMatchingTokensError,
    NoMatchingPatternsError,
)


@pytest.mark.parametrize("test_input, expected", [
    (
        "",
        [],
    ),
    (
        "//",
        ["//"],
    ),
    (
        "hello world!",
        ["hello", "world!"],
    ),
    (
        "    foo    bar     baz    ",
        ["foo", "bar", "baz"],
    ),
    (
        "word",
        ["word"],
    ),
])
def test_get_words_from_line(test_input, expected):
    assert assembler.get_words_from_line(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [
    (
        "",
        "",
    ),
    (
        "//",
        "",
    ),
    (
        "/hello /world!",
        "/hello /world!",
    ),
    (
        "blah blah//",
        "blah blah",
    ),
    (
        "before//after",
        "before",
    ),
    (
        "   before   //after   ",
        "   before   ",
    ),
    (
        "LOAD [A] B",
        "LOAD [A] B",
    ),
])
def test_remove_comments(test_input, expected):
    assert assembler.remove_comments(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [
    (
        "!ALIAS",
        [ALIAS],
    ),
    (
        "!ALIAS0  !ALIAS1",
        [ALIAS, ALIAS],
    ),
    (
        "!ALIAS0  #123",
        [ALIAS, NUMBER],
    ),
])
def test_get_tokens(test_input, expected):
    result_types = [type(result) for result in assembler.get_tokens(test_input)]
    assert result_types == expected


@pytest.mark.parametrize("test_input", [
    "fegwkefjghwfjkhgwekjfgh",
])
def test_get_tokens_raises(test_input):
    with pytest.raises(NoMatchingTokensError):
        assembler.get_tokens(test_input)


@pytest.mark.parametrize("test_input, expected", [
    (
        [ALIAS.from_string("!ALIAS"), NUMBER.from_string("#123")],
        AliasDefinition
    ),
])
def test_get_pattern(test_input, expected):
    assert type(assembler.get_pattern(test_input) == expected)


@pytest.mark.parametrize("test_input", [
    [
        ALIAS.from_string("!ALIAS"),
        ALIAS.from_string("!ALIAS"),
        ALIAS.from_string("!ALIAS")
    ],
])
def test_get_pattern_raises(test_input):
    with pytest.raises(NoMatchingPatternsError):
        assembler.get_pattern(test_input)

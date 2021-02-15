import pytest

from sixteen_bit_computer import new_assembler
from sixteen_bit_computer.assembly_tokens import (
    ALIAS,
    NUMBER,
    OPCODE,
    MODULE,
)
from sixteen_bit_computer.assembly_patterns import (
    NullPattern,
    AliasDefinition,
    Instruction,
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
    assert new_assembler.get_words_from_line(test_input) == expected


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
    assert new_assembler.remove_comments(test_input) == expected


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
    (
        "SET_ZERO  ACC",
        [OPCODE, MODULE],
    ),
])
def test_get_tokens(test_input, expected):
    result_types = [type(result) for result in new_assembler.get_tokens(test_input)]
    assert result_types == expected


@pytest.mark.parametrize("test_input", [
    "fegwkefjghwfjkhgwekjfgh",
])
def test_get_tokens_raises(test_input):
    with pytest.raises(NoMatchingTokensError):
        new_assembler.get_tokens(test_input)


@pytest.mark.parametrize("test_input, expected", [
    (
        [ALIAS.from_string("!ALIAS"), NUMBER.from_string("#123")],
        AliasDefinition
    ),
    (
        [OPCODE.from_string("NOOP")],
        Instruction
    ),
    (
        [OPCODE.from_string("SET_ZERO"), MODULE.from_string("ACC")],
        Instruction
    ),
    (
        [],
        NullPattern
    ),
])
def test_get_pattern(test_input, expected):
    assert isinstance(new_assembler.get_pattern(test_input), expected)


@pytest.mark.parametrize("test_input", [
    [
        ALIAS.from_string("!ALIAS"),
        ALIAS.from_string("!ALIAS"),
        ALIAS.from_string("!ALIAS")
    ],
])
def test_get_pattern_raises(test_input):
    with pytest.raises(NoMatchingPatternsError):
        new_assembler.get_pattern(test_input)

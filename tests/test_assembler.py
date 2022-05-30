import pytest
import textwrap
from sixteen_bit_computer import assembler
from sixteen_bit_computer.assembly_tokens import (
    ALIAS,
    NUMBER,
    OPCODE,
    MODULE,
)
from sixteen_bit_computer.assembly_patterns import (
    NullPattern,
    AliasDef,
    Instruction,
)
from sixteen_bit_computer.exceptions import (
    AssemblyError,
    NoMatchingTokensError,
    NoMatchingPatternsError,
)

# Test what happens when there is no assembly that follows a variable
# or label


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
        "  !ALIAS0  #123   ",
        [ALIAS, NUMBER],
    ),
    (
        "SET_ZERO     ACC",
        [OPCODE, MODULE],
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
        AliasDef
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
    assert isinstance(assembler.get_pattern(test_input), expected)


@pytest.mark.parametrize("test_input", [
    [
        ALIAS.from_string("!ALIAS"),
        ALIAS.from_string("!ALIAS"),
        ALIAS.from_string("!ALIAS"),
    ],
])
def test_get_pattern_raises(test_input):
    with pytest.raises(NoMatchingPatternsError):
        assembler.get_pattern(test_input)


def test_ingest_raw_assembly_lines():
    raw = textwrap.dedent(
        """\
        NOOP
        NOOP
        // A comment
            !myalias #123
        """
    ).splitlines()
    expected = [
        (
            1,
            "NOOP",
            Instruction,
        ),
        (
            2,
            "NOOP",
            Instruction,
        ),
        (
            3,
            "// A comment",
            NullPattern,
        ),
        (
            4,
            "    !myalias #123",
            AliasDef,
        ),
    ]
    processed = assembler.ingest_raw_assembly_lines(raw)
    assert len(processed) == len(raw)
    for assembly_line, result in zip(processed, expected):
        assert assembly_line.line_no == result[0]
        assert assembly_line.raw_line == result[1]
        assert isinstance(assembly_line.pattern, result[2])


@pytest.mark.parametrize("test_input", [
    textwrap.dedent(
        """\
        NOOP
        NOOP
        // A comment
            !myalias #123
            !myalias #456
        """
    ).splitlines(),
    textwrap.dedent(
        """\
            !foobar #0b1010
        NOOP
        // A comment
            !myalias #123
            !foobar #456
        """
    ).splitlines(),
])
def test_check_for_duplicate_alias_names_raises(test_input):
    processed = assembler.ingest_raw_assembly_lines(test_input)
    with pytest.raises(AssemblyError):
        assembler.check_for_duplicate_alias_names(processed)


@pytest.mark.parametrize("test_input", [
    textwrap.dedent(
        """\
        NOOP
        NOOP
        // A comment
            !myalias #123
            !otheralias #456
        """
    ).splitlines(),
    textwrap.dedent(
        """\
            !foobar #0b1010
        NOOP
        // A comment
            !myalias #123
            !hello #456
        """
    ).splitlines(),
])
def test_check_for_duplicate_alias_names_doesnt_raise(test_input):
    processed = assembler.ingest_raw_assembly_lines(test_input)
    assembler.check_for_duplicate_alias_names(processed)


@pytest.mark.parametrize("test_input", [
    textwrap.dedent(
        """\
        &label_0
        &label_1
        &label_0

            NOOP
            NOOP
            // A comment
        """
    ).splitlines(),

    textwrap.dedent(
        """\
            NOOP
            NOOP
            // A comment

        &label_0
        &label_1
        &label_0
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        &label1
            NOOP

        &label2
            // A comment
            SET_ZERO A

        &label1
            NOOP
            SET_ZERO B
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        &label1

            // A comment
            SET_ZERO A

        &label2
            NOOP
            SET_ZERO B

        &label1
            NOOP
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        &label1

            // A comment
            SET_ZERO A

        &label2
            NOOP
            SET_ZERO B

        &label2
            NOOP
        """
    ).splitlines(),
])
def test_check_for_duplicate_label_names_raises(test_input):
    processed = assembler.ingest_raw_assembly_lines(test_input)
    with pytest.raises(AssemblyError):
        assembler.check_for_duplicate_label_names(processed)


@pytest.mark.parametrize("test_input",  [
    textwrap.dedent(
        """\
        &label_0
        &label_1
        &label_2

            NOOP
            NOOP
            // A comment
        """
    ).splitlines(),

    textwrap.dedent(
        """\
            NOOP
            NOOP
            // A comment

        &label_0
        &label_1
        &label_2
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        &label1
            NOOP

        &label2
            // A comment
            SET_ZERO A

        &label3
            NOOP
            SET_ZERO B
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        &label1

            // A comment
            SET_ZERO A

        &label2
            NOOP
            SET_ZERO B

        &label3
            NOOP
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        &label1

            // A comment
            SET_ZERO A

        &label2
            NOOP
            SET_ZERO B

        &label3
            NOOP
        """
    ).splitlines(),
])
def test_check_check_for_duplicate_label_names_doesnt_raise(test_input):
    processed = assembler.ingest_raw_assembly_lines(test_input)
    assembler.check_for_duplicate_label_names(processed)


@pytest.mark.parametrize("test_input", [
    "@ #987654",
    "!alias #-70000",
    "$variable #123 #-40000",
    "ADD #100000",
    "AND [#100000]",
])
def test_check_numbers_in_range_raises(test_input):
    processed = assembler.ingest_raw_assembly_lines([test_input])
    with pytest.raises(AssemblyError):
        assembler.check_numbers_in_range(processed)


@pytest.mark.parametrize("test_input", [
    "@ #987",
    "!alias #-700",
    "$variable #123 #-10000",
    "ADD #0b1111111111",
    "AND [#45]",
])
def test_check_numbers_in_range_doesnt_raise(test_input):
    processed = assembler.ingest_raw_assembly_lines([test_input])
    assembler.check_numbers_in_range(processed)

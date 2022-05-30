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
def test_check_multiple_alias_defs_raises(test_input):
    processed = assembler.ingest_raw_assembly_lines(test_input)
    with pytest.raises(AssemblyError):
        assembler.check_multiple_alias_defs(processed)


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
def test_check_multiple_alias_defs_doesnt_raise(test_input):
    processed = assembler.ingest_raw_assembly_lines(test_input)
    assembler.check_multiple_alias_defs(processed)


@pytest.mark.parametrize("test_input", [
    textwrap.dedent(
        """\
        $marker_0 #123
        $marker_1 #456
        $marker_0 #456

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

        $marker_0 #123
        $marker_1 #456
        $marker_0 #456
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        $marker1 #0b1010
            NOOP

        $marker2 #456
            // A comment
            SET_ZERO A

        $marker1 #45
            NOOP
            SET_ZERO B
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        $marker1 #123

            // A comment
            SET_ZERO A

        $marker2
            NOOP
            SET_ZERO B

        $marker1 #0b1010
            NOOP
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        $marker1 #123

            // A comment
            SET_ZERO A

        $marker2
            NOOP
            SET_ZERO B

        $marker2
            NOOP
        """
    ).splitlines(),
])
def test_check_multiple_marker_defs_raises(test_input):
    processed = assembler.ingest_raw_assembly_lines(test_input)
    with pytest.raises(AssemblyError):
        assembler.check_multiple_marker_defs(processed)


@pytest.mark.parametrize("test_input",  [
    textwrap.dedent(
        """\
        $marker_0 #123
        $marker_1 #456
        $marker_2 #456

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

        $marker_0 #123
        $marker_1 #456
        $marker_2 #456
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        $marker1 #0b1010
            NOOP

        $marker2 #456
            // A comment
            SET_ZERO A

        $marker3 #45
            NOOP
            SET_ZERO B
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        $marker1 #123

            // A comment
            SET_ZERO A

        $marker2
            NOOP
            SET_ZERO B

        $marker3 #0b1010
            NOOP
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        $marker1 #123

            // A comment
            SET_ZERO A

        $marker2
            NOOP
            SET_ZERO B

        $marker3
            NOOP
        """
    ).splitlines(),
])
def test_check_multiple_marker_defs_doesnt_raise(test_input):
    processed = assembler.ingest_raw_assembly_lines(test_input)
    assembler.check_multiple_marker_defs(processed)


@pytest.mark.parametrize("test_input", [
    textwrap.dedent(
        """\
        $marker0
            NOOP

        $marker1
        $marker2
            NOOP
            // A comment
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        $marker1 #0b1010
            NOOP

        $marker2 #456
        $marker3
        $marker4
            // A comment
            SET_ZERO A
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        $marker1 #0b1010
            NOOP

        $marker2 #456
        $marker3
        $marker3
            // A comment
            SET_ZERO A
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        $marker1 #123
            // A comment
            SET_ZERO A

        $marker2
            // A comment

        $marker3
            SET_ZERO B

        $marker4 #0b1010
            NOOP
        """
    ).splitlines(),
])
def test_check_multiple_marker_assignment_raises(test_input):
    processed = assembler.ingest_raw_assembly_lines(test_input)
    with pytest.raises(AssemblyError):
        assembler.check_multiple_marker_assignment(processed)


@pytest.mark.parametrize("test_input", [
    textwrap.dedent(
        """\
        $marker0
            NOOP

        $marker1
            NOOP
            // A comment
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        $marker1 #0b1010
            NOOP

        $marker2 #456
        $marker3
            // A comment
            SET_ZERO A
        """
    ).splitlines(),

    textwrap.dedent(
        """\
        $marker1 #123
            // A comment
            SET_ZERO A

        $marker2
            // A comment

            SET_ZERO B

        $marker4 #0b1010
            NOOP
        """
    ).splitlines(),
])
def test_check_multiple_marker_assignment_doesnt_raise(test_input):
    processed = assembler.ingest_raw_assembly_lines(test_input)
    assembler.check_multiple_marker_assignment(processed)


@pytest.mark.parametrize("test_input", [
    ("!alias #-70000",),
    ("$marker #0xBEEEEF",),
    ("DATA #123 #-40000",),
    ("ADD #100000",),
    ("AND [#100000]",),
])
def test_check_numbers_in_range_raises(test_input):
    processed = assembler.ingest_raw_assembly_lines(test_input)
    with pytest.raises(AssemblyError):
        assembler.check_numbers_in_range(processed)


@pytest.mark.parametrize("test_input", [
    ("!alias #-700",),
    ("$marker #0xBEEF",),
    ("DATA #123 #-10000",),
    ("ADD #0b1111111111",),
    ("AND [#45]",),
])
def test_check_numbers_in_range_doesnt_raise(test_input):
    processed = assembler.ingest_raw_assembly_lines(test_input)
    assembler.check_numbers_in_range(processed)

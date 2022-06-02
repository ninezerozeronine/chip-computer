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


@pytest.mark.parametrize("test_input", [

    """\
        NOOP
        NOOP
    // A comment
    @ #-1
        !myalias #123
        !myalias #456
    """
    ,

    """\
        !foobar #0b1010
    NOOP
    @ #500000
    // A comment
        !myalias #123
        !foobar #456
    """
    ,
])
def test_check_anchors_are_in_range_raises(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    with pytest.raises(AssemblyError):
        assembler.check_anchors_are_in_range(processed)


@pytest.mark.parametrize("test_input", [
    """\
        NOOP
        NOOP
    // A comment
    @ #0
        !myalias #123
        !myalias #456
    """
    ,

    """\
        !foobar #0b1010
    NOOP
    @ #65535
    // A comment
        !myalias #123
        !foobar #456
    """
    ,

    """\
        !foobar #0b1010
    @ #5000
    NOOP
    @ #13
    // A comment
        !myalias #123
        !foobar #456
    """
    ,
])
def test_check_anchors_are_in_range_doesnt_raise(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.check_anchors_are_in_range(processed)


@pytest.mark.parametrize("test_input", [
    """\
    NOOP
    NOOP
    // A comment
        !myalias #123
        !myalias #456
    """
    ,

    """\
        !foobar #0b1010
    NOOP
    // A comment
        !myalias #123
        !foobar #456
    """
])
def test_check_for_duplicate_alias_names_raises(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    with pytest.raises(AssemblyError):
        assembler.check_for_duplicate_alias_names(processed)


@pytest.mark.parametrize("test_input", [
    """\
    NOOP
    NOOP
    // A comment
        !myalias #123
        !otheralias #456
    """
    ,

    """\
        !foobar #0b1010
    NOOP
    // A comment
        !myalias #123
        !hello #456
    """
])
def test_check_for_duplicate_alias_names_doesnt_raise(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.check_for_duplicate_alias_names(processed)


@pytest.mark.parametrize("test_input", [
    """\
    &label_0
    &label_1
    &label_0

        NOOP
        NOOP
        // A comment
    """
    ,

    """\
        NOOP
        NOOP
        // A comment

    &label_0
    &label_1
    &label_0
    """
    ,

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
    ,

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
    ,

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
])
def test_check_for_duplicate_label_names_raises(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    with pytest.raises(AssemblyError):
        assembler.check_for_duplicate_label_names(processed)


@pytest.mark.parametrize("test_input",  [
    """\
    &label_0
    &label_1
    &label_2

        NOOP
        NOOP
        // A comment
    """
    ,

    """\
        NOOP
        NOOP
        // A comment

    &label_0
    &label_1
    &label_2
    """
    ,

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
    ,

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
    ,

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
])
def test_check_for_duplicate_label_names_doesnt_raise(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.check_for_duplicate_label_names(processed)


@pytest.mark.parametrize("test_input", [
    """\
    $var_0
    $var_1 #1 #34 #0xFF
    $var_0

        NOOP
        NOOP
        // A comment
    """
    ,

    """\
        NOOP
        NOOP
        // A comment

    $var_0
    $var_1
    $var_0
    """
    ,

    """\
    $var1
        NOOP

    $var2
        // A comment
        SET_ZERO A

    $var1
        NOOP
        SET_ZERO B
    """
    ,

    """\
    $var1

        // A comment
        SET_ZERO A

    $var2
        NOOP
        SET_ZERO B
        ADD [$var1]

    $var1
        NOOP
    """
    ,

    """\
    $var1

        // A comment
        SET_ZERO A

    $var2
        NOOP
        SET_ZERO B
        ADD [$var1]

    $var2
        NOOP
    """
])
def test_check_for_duplicate_variable_names_raises(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    with pytest.raises(AssemblyError):
        assembler.check_for_duplicate_variable_names(processed)


@pytest.mark.parametrize("test_input",  [
    """\
    $var_0
    $var_1
    $var_2

        NOOP
        NOOP
        // A comment
    """
    ,

    """\
        NOOP
        NOOP
        // A comment

    $var_0
    $var_1
    $var_2
    """
    ,

    """\
    $var1
        NOOP

    $var2
        // A comment
        SET_ZERO A
        ADD [$var1]

    $var3
        NOOP
        SET_ZERO B
    """
    ,

    """\
    @ #32
    $var1 #23 #2

        // A comment
        SET_ZERO A

    $var2
        NOOP
        SET_ZERO B

    $var3 #34 #1
        NOOP
    """
    ,

    """\
    $var1

        // A comment
        SET_ZERO A

    $var2
        NOOP
        SET_ZERO B
        ADD [$var2]

    $var3
        NOOP
    """
])
def test_check_for_duplicate_variable_names_doesnt_raise(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.check_for_duplicate_variable_names(processed)


@pytest.mark.parametrize("test_input, expected", [
    (
        """\
        ADD A
        """,
        [
            0,
        ]
    ),
    (
        """\
        ADD A
        ADD B
        """,
        [
            0, 1
        ]
    ),
    (
        """\
        @ #5
        NOOP

        @ #10
        ADD B
        """,
        [
            5, 10
        ]
    ),
    (
        """\
        @ #5
        NOOP
        $variable
        ADD A

        @ #10
        ADD B

        $data #12 #5
        """,
        [
            5, 7, 10, 11, 12
        ]
    ),
])
def test_assign_machinecode_indecies(test_input, expected):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.assign_machinecode_indecies(processed)
    expected_index = 0
    for assembly_line in processed:
        for word in assembly_line.pattern.machinecode:
            assert word.index == expected[expected_index]
            expected_index += 1


@pytest.mark.parametrize("test_input", [
    """\
    @ #10
        NOOP
    @ #10
        NOOP
        // A comment
    """
    ,

    """\
        NOOP
        NOOP
        // A comment

    $var_0 #1 #2 #3 #4
    @ #2
        NOOP
    """
    ,

    """\
    $var
    @ #10
        NOOP
        ADD A
        ADD #13
        AND [$var]
    @ #12
        SET_ZERO A
    """
])
def test_check_for_colliding_indecies_raises(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.assign_machinecode_indecies(processed)
    with pytest.raises(AssemblyError):
        assembler.check_for_colliding_indecies(processed)


@pytest.mark.parametrize("test_input",  [
    """\
    $var_0
    $var_1 #1 #2 #3
    $var_2

        NOOP
        NOOP
        // A comment
    """
    ,

    """\
    @ #10
        NOOP
        NOOP
    @ #12
        ADD B
    """
    ,

    """\
    $var1
        NOOP

    $var2
        // A comment
        SET_ZERO A
        ADD [$var1]

    $var3
        NOOP
        SET_ZERO B
    """
])
def test_check_for_colliding_indecies_doesnt_raise(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.assign_machinecode_indecies(processed)
    assembler.check_for_colliding_indecies(processed)


@pytest.mark.parametrize("test_input", [
    """\
    @ #-10
        NOOP
    @ #10
        NOOP
        // A comment
    """
    ,

    """\
        NOOP
        NOOP
        // A comment
    @ #65534
    $var_0 #1 #2 #3 #4
        NOOP
    """
    ,

    """\
    $var
    @ #700000
        NOOP
        ADD A
        ADD #13
        AND [$var]
    """
])
def test_check_for_out_of_range_indecies_raises(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.assign_machinecode_indecies(processed)
    with pytest.raises(AssemblyError):
        assembler.check_for_out_of_range_indecies(processed)


@pytest.mark.parametrize("test_input",  [
    """\
    $var_0
    $var_1 #1 #2 #3
    $var_2

        NOOP
        NOOP
        // A comment
    @ #65535
        NOOP
    """
    ,

    """\
    @ #0
        NOOP
        NOOP
    @ #12345
    """
])
def test_check_for_out_of_range_indecies_doesnt_raise(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.assign_machinecode_indecies(processed)
    assembler.check_for_out_of_range_indecies(processed)


@pytest.mark.parametrize("test_input, expected", [
    (
        """\
            ADD #34
        """,
        [
            34,
        ]
    ),
    (
        """\
            NOOP
            ADD A
        $var #1 #2 #3
            ADD B
        """,
        [
            1, 2, 3
        ]
    ),
    (
        """\
        @ #5
            NOOP

        @ #10
            ADD B

        $var #5 #6 #7

        @ #20
        ADD #12
        """,
        [
            5, 6, 7, 12
        ]
    ),
    (
        """\
        @ #5
        NOOP
        $variable
        ADD [#13]

        @ #10
        ADD B

        $data #12 #5
        """,
        [
            13, 12, 5
        ]
    ),
])
def test_resolve_numbers(test_input, expected):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.resolve_numbers(processed)
    expected_index = 0
    for line in processed:
        for word in line.pattern.machinecode:
            if word.const_token:
                assert word.value == expected[expected_index]
                expected_index += 1
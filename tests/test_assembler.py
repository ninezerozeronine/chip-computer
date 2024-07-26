import pytest
import textwrap
from sixteen_bit_computer import assembler
from sixteen_bit_computer.instruction_components import (
    NOOP,
    SET_ZERO,
    ADD,
    AND,
    ACC,
    A,
    B,
    C,
    CONST,
    M_CONST,
)
from sixteen_bit_computer.assembly_tokens import (
    ALIAS,
    NUMBER,
    OPCODE,
    MODULE,
    LABEL,
    VARIABLE
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
from sixteen_bit_computer.instruction_listings import (
    get_instruction_index
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
        NOOP
        NOOP
        // A comment

    &label_0
        AND A
    """
    ,

    """\
    &label1
        NOOP
        NOOP
        // A comment

    &label2
    $var
        NOOP

    &label1
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
    &label1
        // A comment
        SET_ZERO A

    &label2
        NOOP
        SET_ZERO B
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
    $var_1
    &label2
        // A comment
        SET_ZERO A

    &label3
        NOOP
        SET_ZERO B
    """
    ,
    """\
    &label_4
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

        // A comment
        SET_ZERO A

    &label2
    &label4
        NOOP
        SET_ZERO B

    &label3
        NOOP
    """
])
def test_check_for_multiple_label_assignment_raises(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    with pytest.raises(AssemblyError):
        assembler.check_for_multiple_label_assignment(processed)


@pytest.mark.parametrize("test_input",  [
    """\
    &label0
    
        NOOP
        NOOP
        // A comment
    &label1
    """
    ,

    """\
        NOOP
    &label1
        NOOP
        // A comment

    &label0
    """
    ,

    """\
    &label1
    $var_1 #12
    &label2
        // A comment
        SET_ZERO A

    &label3
        NOOP
        SET_ZERO B
    """
    ,
    """\
    &label0
        NOOP
    $var1
        NOOP
        // A comment


    &label1
    // A comment
    $var #1 #2
        NOOP
    &label2
        // A comment
        AND A
    """
])
def test_check_for_multiple_label_assignment_doesnt_raise(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.check_for_multiple_label_assignment(processed)


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
        &label1
            ADD A

        @ #10
        &label2
        // Comment
            ADD B

        $var1 #12 #5
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


@pytest.mark.parametrize("test_input, expected", [
    (
        """\
            ADD #34
        """,
        {}
    ),
    (
        """\
        !first #34
            ADD A

        $var #1 #2 #3
            ADD B

        !second #0b101
        """,
        {
            "first":34,
            "second":5
        }
    ),
    (
        """\
        @ #5
            NOOP

        !first #1
        @ #10
            ADD B

        $var #5 #6 #7

        @ #20
        ADD !first

        !second #34
        """,
        {
            "first":1,
            "second":34
        }
    ),
])
def test_build_alias_map(test_input, expected):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    alias_map = assembler.build_alias_map(processed)
    assert alias_map == expected


@pytest.mark.parametrize("test_input, expected", [
    (
        """\
            !first #1
            ADD !first
        """,
        [1]
    ),
    (
        """\
            ADD !first
        !first #34

        $var #1 #2 #3
            ADD B

        !second #0b101
        """,
        [34]
    ),
    (
        """\
        !one #1
        !two #2
        !three #3
            NOOP

        !first #55
        @ #10
            ADD B

        $var #42 !one !two !three

        @ #20
        ADD !first
        AND !second

        !second #34

        AND !second

        ADD [!one]
        """,
        [1, 2, 3, 55, 34, 34, 1]
    ),
])
def test_resolve_aliases(test_input, expected):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    alias_map = assembler.build_alias_map(processed)
    assembler.resolve_aliases(processed, alias_map)
    expected_index = 0
    for line in processed:
        for word in line.pattern.machinecode:
            if isinstance(word.const_token, ALIAS):
                assert word.value == expected[expected_index]
                expected_index += 1


@pytest.mark.parametrize("test_input", [
    """\
    !first #1
        NOOP
        ADD !second
    """,

    """\
    !first #1
        NOOP
        ADD [!second]
    """,
])
def test_resolve_aliases_raises(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.assign_machinecode_indecies(processed)
    alias_map = assembler.build_alias_map(processed)
    with pytest.raises(AssemblyError):
        assembler.resolve_aliases(processed, alias_map)


@pytest.mark.parametrize("test_input, expected", [
    (
        """\
            ADD #34
        """,
        {}
    ),
    (
        """\
        &first
            ADD A

        $var #1 #2 #3
            ADD B

        &second
        """,
        {
            "first":0,
        }
    ),
    (
        """\
        @ #5
        &first
            NOOP
            NOOP
            ADD A
            ADD #1
            ADD [#2]

        &second
            NOOP
        """,
        {
            "first":5,
            "second":12
        }
    ),
    (
        """\
        @ #5
        &first
            NOOP
            NOOP

        $var

        &second
            ADD A

        $var #1 #2 #2 #4

        &third
            ADD #1
            ADD &first

        &fourth
            NOOP
        """,
        {
            "first": 5,
            "second": 8,
            "third": 13,
            "fourth": 17,
        }
    ),
    (
        """\
        @ #5
        &first
            NOOP
            NOOP

        $var

        &second
            ADD A

        $var #1 #2 #2 #4

        &third
            ADD #1
            ADD &first

        &fourth
        $var2
            NOOP

        $var3 #12
        &fifth
            ADD A
        """,
        {
            "first": 5,
            "second": 8,
            "third": 13,
            "fourth": 18,
            "fifth": 20,
        }
    ),
])
def test_build_label_map(test_input, expected):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.assign_machinecode_indecies(processed)
    label_map = assembler.build_label_map(processed)
    assert label_map == expected


@pytest.mark.parametrize("test_input, expected", [
    (
        """\
        &first
            ADD &first
            NOOP

        @ #10
        &second
            AND [&second]

        """,
        [0, 10]
    ),
    (
        """\
            ADD &first
            AND [&first]
        
        &second
        $var1 #1 #2 #3
            ADD B

        @ #15
        $var2
        &first
            NOOP
            ADD &second
        """,
        [16, 16, 7]
    ),
])
def test_resolve_labels(test_input, expected):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.assign_machinecode_indecies(processed)
    label_map = assembler.build_label_map(processed)
    assembler.resolve_labels(processed, label_map)
    expected_index = 0
    for line in processed:
        for word in line.pattern.machinecode:
            if isinstance(word.const_token, LABEL):
                assert word.value == expected[expected_index]
                expected_index += 1


@pytest.mark.parametrize("test_input", [
    """\
    &label1
        NOOP
        ADD &label2
    """,

    """\
    @ #123
    !first #1
    &label1
        NOOP
        ADD [&label2]
    """,

    """\
    @ #45
    !first #1
        NOOP
        ADD [&label1]

    &label1
    """
])
def test_resolve_labels_raises(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.assign_machinecode_indecies(processed)
    label_map = assembler.build_label_map(processed)
    with pytest.raises(AssemblyError):
        assembler.resolve_labels(processed, label_map)


@pytest.mark.parametrize("test_input, expected", [
    (
        """\
            ADD #34
        """,
        {}
    ),
    (
        """\
        $first
            ADD A
            NOOP

        $second #1 #2 #3
            ADD B

        $third
        """,
        {
            "first": 0,
            "second": 3,
            "third": 7,
        }
    ),
    (
        """\
        @ #5
        $first #1 #2
            NOOP
            NOOP
            ADD A
            ADD #1
            ADD [#2]

        $second
            NOOP
            ADD [$third]

        @ #40
        $third #1

        """,
        {
            "first": 5,
            "second": 14,
            "third": 40
        }
    ),
])
def test_build_variable_map(test_input, expected):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.assign_machinecode_indecies(processed)
    variable_map = assembler.build_variable_map(processed)
    assert variable_map == expected


@pytest.mark.parametrize("test_input, expected", [
    (
        """\
        $var1

        &first
            ADD $var1
            NOOP

        @ #10
        $var2
        &second
            AND [$var1]

            ADD $var2

        """,
        [0, 0, 10]
    ),
    (
        """\
            ADD $var2
            AND [$var3]
        
        &second
        $var1 #1 #2 #3
            ADD B

        @ #15
        $var2
        &first
            NOOP
            ADD $var1
        $var3
        """,
        [15, 19, 4]
    ),
])
def test_resolve_variables(test_input, expected):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.assign_machinecode_indecies(processed)
    variable_map = assembler.build_variable_map(processed)
    assembler.resolve_variables(processed, variable_map)
    expected_index = 0
    for line in processed:
        for word in line.pattern.machinecode:
            if isinstance(word.const_token, VARIABLE):
                assert word.value == expected[expected_index]
                expected_index += 1


@pytest.mark.parametrize("test_input", [
    """\
    $var1
        NOOP
        ADD $var2
    """,

    """\
    @ #123
    !first #1
    &label1
        NOOP
        ADD [$var2]
    $var1 #1 #2
    """,

    """\
    @ #45
    $var1
    !first #1
        NOOP
        ADD $var2

    &label1
    """
])
def test_resolve_variables_raises(test_input):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    processed = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.assign_machinecode_indecies(processed)
    variable_map = assembler.build_variable_map(processed)
    with pytest.raises(AssemblyError):
        assembler.resolve_variables(processed, variable_map)


def test_assemble_all_instructions():
    test_data = """\
        NOOP
        COPY ACC A
        COPY ACC B
        COPY ACC C
        COPY ACC SP
        COPY ACC X
        COPY ACC Y
        COPY ACC Z
        COPY A ACC
        COPY A B
        COPY A C
        COPY B ACC
        COPY B A
        COPY B C
        COPY C ACC
        COPY C A
        COPY C B
        COPY X ACC
        COPY Y ACC
        COPY Z ACC
        COPY PC ACC
        COPY SP ACC
        LOAD [ACC] A
        LOAD [ACC] B
        LOAD [ACC] C
        LOAD [A] ACC
        LOAD [A] B
        LOAD [A] C
        LOAD [B] ACC
        LOAD [B] A
        LOAD [B] C
        LOAD [C] ACC
        LOAD [C] A
        LOAD [C] B
        LOAD [SP] ACC
        LOAD [SP] A
        LOAD [SP] B
        LOAD [SP] C
        LOAD [#123] ACC
        LOAD [#123] A
        LOAD [#123] B
        LOAD [#123] C
        STORE ACC [A]
        STORE ACC [B]
        STORE ACC [C]
        STORE ACC [SP]
        STORE ACC [#456]
        STORE A [ACC]
        STORE A [B]
        STORE A [C]
        STORE A [SP]
        STORE A [#456]
        STORE B [ACC]
        STORE B [A]
        STORE B [C]
        STORE B [SP]
        STORE B [#456]
        STORE C [ACC]
        STORE C [A]
        STORE C [B]
        STORE C [SP]
        STORE C [#456]
        STORE SP [ACC]
        STORE SP [A]
        STORE SP [B]
        STORE SP [C]
        STORE SP [#456]
        PUSH ACC
        PUSH A
        PUSH B
        PUSH C
        POP ACC
        POP A
        POP B
        POP C
        SET ACC #123
        SET A #123
        SET B #123
        SET C #123
        SET SP #123
        SET [#456] #123
        SET_ZERO ACC
        SET_ZERO A
        SET_ZERO B
        SET_ZERO C
        JUMP ACC
        JUMP A
        JUMP B
        JUMP C
        JUMP #123
        JUMP [ACC]
        JUMP [A]
        JUMP [B]
        JUMP [C]
        JUMP [SP]
        JUMP [#456]
        JUMP_IF_ACC_LT A #123
        JUMP_IF_ACC_LT B #123
        JUMP_IF_ACC_LT C #123
        JUMP_IF_ACC_LT #123 #123
        JUMP_IF_ACC_LT [#456] #123
        JUMP_IF_ACC_LTE A #123
        JUMP_IF_ACC_LTE B #123
        JUMP_IF_ACC_LTE C #123
        JUMP_IF_ACC_LTE #123 #123
        JUMP_IF_ACC_LTE [#456] #123
        JUMP_IF_ACC_EQ A #123
        JUMP_IF_ACC_EQ B #123
        JUMP_IF_ACC_EQ C #123
        JUMP_IF_ACC_EQ #123 #123
        JUMP_IF_ACC_EQ [#456] #123
        JUMP_IF_ACC_NEQ A #123
        JUMP_IF_ACC_NEQ B #123
        JUMP_IF_ACC_NEQ C #123
        JUMP_IF_ACC_NEQ #123 #123
        JUMP_IF_ACC_NEQ [#456] #123
        JUMP_IF_ACC_GTE A #123
        JUMP_IF_ACC_GTE B #123
        JUMP_IF_ACC_GTE C #123
        JUMP_IF_ACC_GTE #123 #123
        JUMP_IF_ACC_GTE [#456] #123
        JUMP_IF_ACC_GT A #123
        JUMP_IF_ACC_GT B #123
        JUMP_IF_ACC_GT C #123
        JUMP_IF_ACC_GT #123 #123
        JUMP_IF_ACC_GT [#456] #123
        JUMP_IF_EQ_ZERO ACC #123
        JUMP_IF_EQ_ZERO A #123
        JUMP_IF_EQ_ZERO B #123
        JUMP_IF_EQ_ZERO C #123
        JUMP_IF_NEQ_ZERO ACC #123
        JUMP_IF_NEQ_ZERO A #123
        JUMP_IF_NEQ_ZERO B #123
        JUMP_IF_NEQ_ZERO C #123
        JUMP_IF_NEGATIVE_FLAG #123
        JUMP_IF_NOT_NEGATIVE_FLAG #123
        JUMP_IF_CARRY #123
        JUMP_IF_NOT_CARRY #123
        JUMP_IF_BORROW #123
        JUMP_IF_NOT_BORROW #123
        JUMP_IF_EQUAL_FLAG #123
        JUMP_IF_NOT_EQUAL_FLAG #123
        JUMP_IF_ZERO_FLAG #123
        JUMP_IF_NOT_ZERO_FLAG #123
        CALL ACC
        CALL A
        CALL B
        CALL C
        CALL #123
        RETURN
        HALT
        NOT ACC
        NOT A
        NOT B
        NOT C
        NOT [#456]
        AND A
        AND B
        AND C
        AND #123
        AND [#456]
        NAND A
        NAND B
        NAND C
        NAND #123
        NAND [#456]
        OR A
        OR B
        OR C
        OR #123
        OR [#456]
        NOR A
        NOR B
        NOR C
        NOR #123
        NOR [#456]
        XOR A
        XOR B
        XOR C
        XOR #123
        XOR [#456]
        NXOR A
        NXOR B
        NXOR C
        NXOR #123
        NXOR [#456]
        ROT_LEFT ACC
        ROT_LEFT A
        ROT_LEFT B
        ROT_LEFT C
        ROT_LEFT [#456]
        ROT_RIGHT ACC
        ROT_RIGHT A
        ROT_RIGHT B
        ROT_RIGHT C
        ROT_RIGHT [#456]
        SHIFT_LEFT ACC
        SHIFT_LEFT A
        SHIFT_LEFT B
        SHIFT_LEFT C
        SHIFT_LEFT [#456]
        SHIFT_RIGHT ACC
        SHIFT_RIGHT A
        SHIFT_RIGHT B
        SHIFT_RIGHT C
        SHIFT_RIGHT [#456]
        ADD A
        ADD B
        ADD C
        ADD #123
        ADD [#456]
        // ADDC A
        // ADDC B
        // ADDC C
        // ADDC #123
        // ADDC [#456]
        SUB A
        SUB B
        SUB C
        SUB #123
        SUB [#456]
        // SUBB A
        // SUBB B
        // SUBB C
        // SUBB #123
        // SUBB [#456]
        INCR ACC
        INCR A
        INCR B
        INCR C
        INCR [#456]
        DECR ACC
        DECR A
        DECR B
        DECR C
        DECR [#456]
        STORE_INCR ACC [A] [B]
        STORE_INCR #123 [A] [B]
        STORE_DECR ACC [A] [B]
        STORE_DECR #123 [A] [B]
    """
    dedent_and_split = textwrap.dedent(test_data).splitlines()
    assembler.assemble(dedent_and_split)
    assert True

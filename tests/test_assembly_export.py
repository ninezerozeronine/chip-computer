import pytest
import textwrap


from sixteen_bit_computer import (
    assembler,
    assembly_export
)
from sixteen_bit_computer.instruction_listings import (
    get_instruction_index
)
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


@pytest.mark.parametrize("test_input, expected", [
    (
        """\
        // A comment

        &label2
        !an_alias #23

        $variable

        &label1

        @ #54
        """,
        {}
    ),
    (
        """\
            ADD #34
        """,
        {
            0: get_instruction_index((ADD, CONST)),
            1: 34,
        }
    ),
    (
        """\
        @ #10
            ADD #34
            NOOP
        $var1
        $var2 #5
        """,
        {
            10: get_instruction_index((ADD, CONST)),
            11: 34,
            12: get_instruction_index((NOOP,)),
            14: 5,
        }
    ),
    (
        """\
        &label0
            ADD A
            NOOP

        $second #1 #2 !alias2
            ADD B

            ADD [&label0]
            AND [!alias0]
        !alias0 #25

        // A comment
        @ #456
            AND C

        !alias2 #999
        """,
        {
            0: get_instruction_index((ADD, A)),
            1: get_instruction_index((NOOP,)),
            2: 1,
            3: 2,
            4: 999,
            5: get_instruction_index((ADD, B)),
            6: get_instruction_index((ADD, M_CONST)),
            7: 0,
            8: get_instruction_index((AND, M_CONST)),
            9: 25,
            456: get_instruction_index((AND, C)),
        }
    ),
])
def test_assembly_lines_to_dictionary(test_input, expected):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    lines = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.process_assembly_lines(lines)
    res = assembly_export.assembly_lines_to_dictionary(lines)
    assert res == expected

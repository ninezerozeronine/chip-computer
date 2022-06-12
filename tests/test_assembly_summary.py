import pytest
import textwrap

from sixteen_bit_computer import (
    assembler,
    assembly_summary
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


@pytest.mark.parametrize("test_input,expected", [
    (
        """\
        // A comment

        NOOP
        """,
        [
            {
                "assembly" : {
                    "raw": "// A comment",
                    "line_no": "1"
                }
            },
            {
                "assembly" : {
                    "raw": "",
                    "line_no": "2"
                }
            },
            {
                "assembly" : {
                    "raw": "NOOP",
                    "line_no": "3"
                },
                "word" : {
                    "index_decimal": "0",
                    "index_hex": "0x0000",
                    "value_decimal": str(get_instruction_index((NOOP,))),
                    "value_hex": "0x{:04X}".format(get_instruction_index((NOOP,)))
                }
            }
        ]
    ),
    (
        """\
        @ #10
        &label
            AND &label
            NOOP
        """,
        [
            {
                "assembly" : {
                    "raw": "@ #10",
                    "line_no": "1"
                }
            },
            {
                "assembly" : {
                    "raw": "&label",
                    "line_no": "2"
                }
            },
            {
                "assembly" : {
                    "raw": "    AND &label",
                    "line_no": "3"
                },
                "word" : {
                    "index_decimal": "10",
                    "index_hex": "0x000A",
                    "value_decimal": str(get_instruction_index((AND, CONST))),
                    "value_hex": "0x{:04X}".format(get_instruction_index((AND, CONST))),
                    "label": "&label",

                }
            },
            {
                "word" : {
                    "index_decimal": "11",
                    "index_hex": "0x000B",
                    "value_decimal": str(10),
                    "value_hex": "0x{:04X}".format(10),
                    "const": "&label"
                }
            },
            {
                "assembly" : {
                    "raw": "    NOOP",
                    "line_no": "4"
                },
                "word" : {
                    "index_decimal": "12",
                    "index_hex": "0x000C",
                    "value_decimal": str(get_instruction_index((NOOP,))),
                    "value_hex": "0x{:04X}".format(get_instruction_index((NOOP,)))
                }
            }
        ]
    ),
    (
        """\
        NOOP
        $var #1 #2
        AND A
        """,
        [
            {
                "assembly" : {
                    "raw": "NOOP",
                    "line_no": "1"
                },
                "word" : {
                    "index_decimal": "0",
                    "index_hex": "0x0000",
                    "value_decimal": str(get_instruction_index((NOOP,))),
                    "value_hex": "0x{:04X}".format(get_instruction_index((NOOP,)))
                }
            },
            {
                "assembly" : {
                    "raw": "$var #1 #2",
                    "line_no": "2"
                },
                "word" : {
                    "index_decimal": "1",
                    "index_hex": "0x0001",
                    "value_decimal": str(1),
                    "value_hex": "0x{:04X}".format(1),
                    "const": "#1"
                }
            },
            {
                "word" : {
                    "index_decimal": "2",
                    "index_hex": "0x0002",
                    "value_decimal": str(2),
                    "value_hex": "0x{:04X}".format(2),
                    "const": "#2"
                }
            },
            {
                "assembly" : {
                    "raw": "AND A",
                    "line_no": "3"
                },
                "word" : {
                    "index_decimal": "3",
                    "index_hex": "0x0003",
                    "value_decimal": str(get_instruction_index((AND, A))),
                    "value_hex": "0x{:04X}".format(get_instruction_index((AND, A))),
                }
            },
        ]
    ),
])
def test_get_assembly_summary_data(test_input, expected):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    lines = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.process_assembly_lines(lines)
    label_map = assembler.build_label_map(lines)
    assert assembly_summary.get_assembly_summary_data(lines, label_map) == expected
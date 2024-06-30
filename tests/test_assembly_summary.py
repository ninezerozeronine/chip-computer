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

        !alias #23
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
                    "raw": "!alias #23",
                    "line_no": "3"
                },
            }
        ]
    ),
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


@pytest.mark.parametrize("test_input,expected", [
    (
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
                    "value_decimal": "123",
                    "value_hex": "0x00AF"
                }
            }
        ],
        {
            "asm_line_no": 1,
            "asm_line": 12,
            "word_index_decimal": 1,
            "word_value_decimal": 3,
            "word_label": 0,
        }
    ),
    (
        [
            {
                "assembly" : {
                    "raw": "123456789012345678",
                    "line_no": "1"
                }
            },
            {
                "word" : {
                    "index_decimal": "123",
                    "index_hex": "0xFFFF",
                    "value_decimal": "1234",
                    "value_hex": "0x00AF"
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
                    "line_no": "500"
                },
                "word" : {
                    "index_decimal": "0",
                    "index_hex": "0x0000",
                    "value_decimal": "123",
                    "value_hex": "0x00AF",
                    "label": "mylabel"
                }
            },

        ],
        {
            "asm_line_no": 3,
            "asm_line": 18,
            "word_index_decimal": 3,
            "word_value_decimal": 4,
            "word_label": 7,
        }
    )
])
def test_get_widest_column_values(test_input, expected):
    assert assembly_summary.get_widest_column_values(test_input) == expected

@pytest.mark.parametrize("test_input,expected", [
    (
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
                    "raw": "!alias #23",
                    "line_no": "3"
                },
            }
        ],
        [
            "1 // A comment |",
            "2              |",
            "3 !alias #23   |",
        ]
    ),
    (
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
                    "value_decimal": "123",
                    "value_hex": "0x00AF"
                }
            }
        ],
        [
            "1 // A comment |",
            "2              |",
            "3 NOOP         | 0 0x0000 - 123 0x00AF",
        ]
    ),
    (
        [
            {
                "assembly" : {
                    "raw": "// A comment",
                    "line_no": "1",
                }
            },
            {
                "assembly" : {
                    "raw": "",
                    "line_no": "2",
                }
            },
            {
                "assembly" : {
                    "raw": "@ #123",
                    "line_no": "3",
                }
            },
            {
                "assembly" : {
                    "raw": "    FOOBAR",
                    "line_no": "555",
                },
                "word" : {
                    "index_decimal": "123",
                    "index_hex": "0xFFFE",
                    "value_decimal": "13",
                    "value_hex": "0x00AF",
                    "label": "&mylabel",
                }
            },
            {
                "word" : {
                    "index_decimal": "3",
                    "index_hex": "0x0003",
                    "value_decimal": "123",
                    "value_hex": "0xBEEF",
                    "label": "&myotherlabel",
                    "const": "!alias",
                }
            },
            {
                "assembly" : {
                    "raw": "    NOOP",
                    "line_no": "6"
                },
                "word" : {
                    "index_decimal": "0",
                    "index_hex": "0x0000",
                    "value_decimal": "1",
                    "value_hex": "0x00FF"
                }
            }
        ],
        [
            "  1 // A comment |",
            "  2              |",
            "  3 @ #123       |",
            "555     FOOBAR   | 123 0xFFFE - &mylabel       13 0x00AF",
            "                 |   3 0x0003 - &myotherlabel 123 0xBEEF !alias",
            "  6     NOOP     |   0 0x0000 -                 1 0x00FF",
        ]
    ),
])
def test_generate_assembly_summary_lines(test_input, expected):
    assert assembly_summary.generate_assembly_summary_lines(test_input) == expected
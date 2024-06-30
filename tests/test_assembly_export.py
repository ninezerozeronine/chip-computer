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

def test_generate_arduino_header():
    expected = textwrap.dedent(
        """\
        #ifndef PROG_PROGNAME_H
        #define PROG_PROGNAME_H

        #include <Arduino.h>

        extern const unsigned int num_progname_words;
        extern const unsigned int progname_addresses[];
        extern const unsigned int progname_words[];

        extern const char progname_program_name[];

        #endif
        """
    )
    assert assembly_export.generate_arduino_header("progname") == expected


def test_generate_arduino_cpp():
    expected = textwrap.dedent(
        """\
        #include "prog_progname.h"

        // Number of words in the program
        extern const unsigned int num_progname_words = 5;

        // Address of each word in the list of machinecode words
        extern const unsigned int progname_addresses[] PROGMEM = {{
            0x0003, // 0x{noop_code:04X} - 0004     NOOP
            0x0004, // 0x{add_a_code:04X} - 0005     ADD A
            0x0005, // 0x{and_mconst_code:04X} - 0006     AND [#0xBEEF]
            0x0006, // 0xBEEF - 0006
            0x000A  // 0x0002 - 0009 $var #2
        }};

        // Value for each machinecode word
        extern const unsigned int progname_words[] PROGMEM = {{
            0x{noop_code:04X}, // 0x0003 - 0004     NOOP
            0x{add_a_code:04X}, // 0x0004 - 0005     ADD A
            0x{and_mconst_code:04X}, // 0x0005 - 0006     AND [#0xBEEF]
            0xBEEF, // 0x0006 - 0006
            0x0002  // 0x000A - 0009 $var #2
        }};

        // Max of seven characters
        extern const char progname_program_name[] = "DEFAULT";
        """
    )

    expected = expected.format(
        noop_code=get_instruction_index((NOOP,)),
        add_a_code=get_instruction_index((ADD, A)),
        and_mconst_code=get_instruction_index((AND, M_CONST)),
    )

    raw_assembly = textwrap.dedent(
        """\
        // A comment

        @ #3
            NOOP
            ADD A
            AND [#0xBEEF]

        @ #10
        $var #2
        """
    )
    dedent_and_split = textwrap.dedent(raw_assembly).splitlines()
    lines = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.process_assembly_lines(lines)

    progname = "progname"
    h_filename = "prog_progname.h"

    assert assembly_export.generate_arduino_cpp(
        lines, progname, h_filename
    ) == expected


def test_get_address_and_word_lines():
    expected_addresses = [
        "    0x0003, // 0x{noop_code:04X} - 0004     NOOP".format(
            noop_code=get_instruction_index((NOOP,))
        ),
        "    0x0004, // 0x{add_a_code:04X} - 0005     ADD A".format(
            add_a_code=get_instruction_index((ADD, A))
        ),
        "    0x0005, // 0x{and_mconst_code:04X} - 0006     AND [#0xBEEF]".format(
            and_mconst_code=get_instruction_index((AND, M_CONST)),
        ),
        "    0x0006, // 0xBEEF - 0006",
        "    0x0007, // 0x{noop_code:04X} - 0007     NOOP".format(
            noop_code=get_instruction_index((NOOP,))
        ),
        "    0x0008, // 0x{and_mconst_code:04X} - 0008     AND &label".format(
            and_mconst_code=get_instruction_index((AND, CONST)),
        ),
        "    0x0009, // 0x000B - 0008",
        "    0x000A, // 0x03E9 - 0011 $var #1001",
        "    0x000B  // 0x{noop_code:04X} - 0014     NOOP".format(
            noop_code=get_instruction_index((NOOP,))
        ),
    ]

    expected_words = [
        "    0x{noop_code:04X}, // 0x0003 - 0004     NOOP".format(
            noop_code=get_instruction_index((NOOP,))
        ),
        "    0x{add_a_code:04X}, // 0x0004 - 0005     ADD A".format(
            add_a_code=get_instruction_index((ADD, A))
        ),
        "    0x{and_mconst_code:04X}, // 0x0005 - 0006     AND [#0xBEEF]".format(
            and_mconst_code=get_instruction_index((AND, M_CONST)),
        ),
        "    0xBEEF, // 0x0006 - 0006",
        "    0x{noop_code:04X}, // 0x0007 - 0007     NOOP".format(
            noop_code=get_instruction_index((NOOP,))
        ),
        "    0x{and_const_code:04X}, // 0x0008 - 0008     AND &label".format(
            and_const_code=get_instruction_index((AND, CONST)),
        ),
        "    0x000B, // 0x0009 - 0008",
        "    0x03E9, // 0x000A - 0011 $var #1001",
        "    0x{noop_code:04X}  // 0x000B - 0014     NOOP".format(
            noop_code=get_instruction_index((NOOP,))
        ),
    ]

    raw_assembly = textwrap.dedent(
        """\
        // A comment

        @ #3
            NOOP
            ADD A
            AND [#0xBEEF]
            NOOP
            AND &label

        @ #10
        $var #1001

        &label
            NOOP
        """
    )
    dedent_and_split = textwrap.dedent(raw_assembly).splitlines()
    lines = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.process_assembly_lines(lines)

    addresses, words = assembly_export.get_address_and_word_lines(lines)
    assert addresses == expected_addresses
    assert words == expected_words


def test_assembly_lines_to_logisim():
    expected = textwrap.dedent(
        """\
        v2.0 raw
        BEEF BEEF BEEF BEEF  BEEF BEEF BEEF BEEF  BEEF BEEF BEEF BEEF  BEEF BEEF BEEF BEEF
        {noop_code:04X} {noop_code:04X} {and_mconst_code:04X} FACE
        """
    )
    expected = expected.format(
        noop_code=get_instruction_index((NOOP,)),
        and_mconst_code=get_instruction_index((AND, M_CONST)),
    )

    raw_assembly = textwrap.dedent(
        """\
        // A comment

        @ #16
            NOOP
            NOOP
            AND [#0xFACE]

        // Another comment
        """
    )
    dedent_and_split = textwrap.dedent(raw_assembly).splitlines()
    lines = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.process_assembly_lines(lines)

    assert assembly_export.assembly_to_logisim(
        lines, default_value=0xBEEF) == expected 


@pytest.mark.parametrize("test_input, expected", [
    (
        """\
        // A comment

        &label2
        !an_alias #23

        $variable

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

@pytest.mark.parametrize("test_input, expected", [
    (
        """\
        // A comment

        &label2
        !an_alias #23

        $variable

        @ #54
        """,
        []
    ),
    (
        """\
            ADD #34
        """,
        [
            (0, get_instruction_index((ADD, CONST))),
            (1, 34),
        ]
    ),
    (
        """\
        @ #10
            ADD #34
            NOOP
        $var1
        $var2 #5
        """,
        [
            (10, get_instruction_index((ADD, CONST))),
            (11, 34),
            (12, get_instruction_index((NOOP,))),
            (14, 5),
        ]
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
        [
            (0, get_instruction_index((ADD, A))),
            (1, get_instruction_index((NOOP,))),
            (2, 1),
            (3, 2),
            (4, 999),
            (5, get_instruction_index((ADD, B))),
            (6, get_instruction_index((ADD, M_CONST))),
            (7, 0),
            (8, get_instruction_index((AND, M_CONST))),
            (9, 25),
            (456, get_instruction_index((AND, C))),
        ]
    ),
])
def test_assembly_lines_to_address_word_pairs(test_input, expected):
    dedent_and_split = textwrap.dedent(test_input).splitlines()
    lines = assembler.ingest_raw_assembly_lines(dedent_and_split)
    assembler.process_assembly_lines(lines)
    res = assembly_export.assembly_lines_to_address_word_pairs(lines)
    assert res == expected

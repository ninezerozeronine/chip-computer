import textwrap

import pytest

from eight_bit_computer import export
from eight_bit_computer.data_structures import (
    get_assembly_line_template, get_machine_code_byte_template
)


def test_bitstrings_to_arduino_cpp():
    test_data = [
        "10111110", "11101111", "11111010", "11001110",    "10111110", "11101111", "11111010", "11001110",    "10111110", "11101111", "11111010", "11001110",    "10111110", "11101111", "11111010", "11001110",
        "00000000", "11111111", "10101010", "01010101",    "10111110", "11101111", "11111010", "11001110",    "10111110", "11101111", "11111010", "11001110",    "10111110", "11101111", "11111010", "11001110",
    ]
    expected = textwrap.dedent(
        """\
        #include "example_header.h"

        extern const byte EXAMPLE_VAR_NAME[] __attribute__ (( __section__(".fini1") )) = {
            0xBE, 0xEF, 0xFA, 0xCE,  0xBE, 0xEF, 0xFA, 0xCE,  0xBE, 0xEF, 0xFA, 0xCE,  0xBE, 0xEF, 0xFA, 0xCE, // 00000
            0x00, 0xFF, 0xAA, 0x55,  0xBE, 0xEF, 0xFA, 0xCE,  0xBE, 0xEF, 0xFA, 0xCE,  0xBE, 0xEF, 0xFA        // 00016
        };
        extern const byte EXAMPLE_VAR_NAME_LAST_BYTE = 0xCE;
        """
    )

    assert export.bitstrings_to_arduino_cpp(test_data, 0, "example_header.h", "EXAMPLE_VAR_NAME") == expected


def test_create_arduino_header():
    expected = textwrap.dedent(
        """\
        #ifndef HEADER_FILENAME_H
        #define HEADER_FILENAME_H

        #include <Arduino.h>

        extern const byte EXAMPLE_VAR_NAME[];
        extern const byte EXAMPLE_VAR_NAME_LAST_BYTE;

        #endif
        """
    )

    assert export.create_arduino_header("header_filename", "EXAMPLE_VAR_NAME") == expected


def generator_tester(generator_iterator_to_test, expected_values):
    """
    https://stackoverflow.com/questions/34346182/testing-a-generator-in-python
    """
    range_index = 0
    for actual in generator_iterator_to_test:
        assert range_index + 1 <= len(expected_values), 'Too many values returned from range'
        assert expected_values[range_index] == actual
        range_index += 1

    assert range_index == len(expected_values), 'Too few values returned from range'


@pytest.mark.parametrize("seq,chunk_size,expected", [
    ([0, 1, 2, 3, 4, 5, 6, 7],   8, [[0, 1, 2, 3, 4, 5, 6, 7]]),
    ([0, 1, 2, 3, 4, 5, 6, 7],   2, [[0, 1], [2, 3], [4, 5], [6, 7]]),
    ([0, 1, 2, 3, 4, 5, 6, 7],   10, [[0, 1, 2, 3, 4, 5, 6, 7]]),
    ([0, 1, 2, 3, 4, 5, 6, 7],   3, [[0, 1, 2], [3, 4, 5], [6, 7]]),
])
def test_chunker(seq, chunk_size, expected):
    generator = export.chunker(seq, chunk_size)
    generator_tester(generator, expected)


def test_gen_logisim_program_file(assembly_line_infos):
    expected = textwrap.dedent(
        """\
        v2.0 raw
        FF 00 FF 01  FF 00 FF 7B  FF 02 FF 00  37 55 00 00
        00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
        00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
        00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
        00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
        00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
        00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
        00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
        00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
        00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
        00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
        00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
        00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
        00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
        00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
        00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
        7B D3 2A
        """
    )

    assert export.gen_logisim_program_file(assembly_line_infos) == expected


def test_extract_machine_code(assembly_line_infos):
    expected = [
        "11111111",
        "00000000",
        "11111111",
        "00000001",

        "11111111",
        "00000000",
        "11111111",
        "01111011",

        "11111111",
        "00000010",
        "11111111",
        "00000000",

        "00110111",
        "01010101",
        "00000000"
    ]
    assert export.extract_machine_code(assembly_line_infos) == expected



def gen_test_extract_variables_data():
    ret = []

    lines = []
    line1 = get_assembly_line_template()
    line1["defines_variable"] = True
    line1["defined_variable"] = "$var1"
    line1["defined_variable_location"] = 0
    line1["defined_variable_value"] = 1
    lines.append(line1)

    res = ["00000001"]

    ret.append((lines, res))


    lines = []
    line1 = get_assembly_line_template()
    line1["defines_variable"] = True
    line1["defined_variable"] = "$var1"
    line1["defined_variable_location"] = 0
    line1["defined_variable_value"] = 1
    lines.append(line1)

    line2 = get_assembly_line_template()
    line2["defines_variable"] = True
    line2["defined_variable"] = "$var2"
    line2["defined_variable_location"] = 1
    line2["defined_variable_value"] = 5
    lines.append(line2)

    res = ["00000001", "00000101"]

    ret.append((lines, res))

    lines = []
    line1 = get_assembly_line_template()
    line1["defines_variable"] = True
    line1["defined_variable"] = "$var1"
    line1["defined_variable_location"] = 2
    line1["defined_variable_value"] = 255
    lines.append(line1)

    res = ["00000000", "00000000", "11111111"]

    ret.append((lines, res))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", gen_test_extract_variables_data()
)
def test_extract_variables(test_input, expected):
    assert export.extract_variables(test_input) == expected


def gen_test_combine_mc_and_variable_bitstrings_data():
    ret = []

    mc_bitstrings = []
    variable_bitstrings = []
    res = []
    ret.append((mc_bitstrings, variable_bitstrings, res))

    mc_bitstrings = ["00001000"]
    variable_bitstrings = []
    res = ["00001000"]
    ret.append((mc_bitstrings, variable_bitstrings, res))

    mc_bitstrings = ["00001000", "00001001"]
    variable_bitstrings = []
    res = ["00001000", "00001001"]
    ret.append((mc_bitstrings, variable_bitstrings, res))

    mc_bitstrings = ["00001000", "00001001"]
    variable_bitstrings = ["00001111"]
    res = (["00001000", "00001001"] + ["00000000"] * 254) + ["00001111"]
    ret.append((mc_bitstrings, variable_bitstrings, res))

    return ret


@pytest.mark.parametrize(
    "mc_bitstrings,variable_bitstrings,expected",
    gen_test_combine_mc_and_variable_bitstrings_data()
)
def test_combine_mc_and_variable_bitstrings(mc_bitstrings, variable_bitstrings, expected):
    assert export.combine_mc_and_variable_bitstrings(mc_bitstrings, variable_bitstrings) == expected


def test_bitstrings_to_logisim():
    test_data = [
        "10111110",
        "11101111",
        "11111010",
        "11001110",
    ]
    expected = textwrap.dedent(
        """\
        v2.0 raw
        BE EF FA CE
        """
    )
    assert export.bitstrings_to_logisim(test_data) == expected


def test_gen_arduino_program_h_file():
    expected = textwrap.dedent(
        """\
        #ifndef PROG_FIBONACCI_H
        #define PROG_FIBONACCI_H

        #include <Arduino.h>

        extern const byte num_fibonacci_program_bytes;
        extern const byte fibonacci_program_bytes[];

        extern const byte num_fibonacci_data_bytes;
        extern const byte fibonacci_data_bytes[];

        extern const char fibonacci_program_name[];

        #endif
        """
    )

    assert export.gen_arduino_program_h_file("fibonacci") == expected


def test_gen_arduino_program_cpp_file(assembly_line_infos):
    expected = textwrap.dedent(
        """\
        #include "prog_fibonacci.h"

        extern const byte num_fibonacci_program_bytes = 15;
        extern const byte fibonacci_program_bytes[] PROGMEM = {
            0xFF, // 000 LOAD [$variable0] A (@label1)
            0x00, // 001 (0)
            0xFF, // 002 LOAD [$variable1] A (@label2)
            0x01, // 003 (1)
            0xFF, // 004 JUMP @label1
            0x00, // 005 (0)
            0xFF, // 006 STORE A [#123]
            0x7B, // 007 (123)
            0xFF, // 008 LOAD [$variable2] B (@label3)
            0x02, // 009 (2)
            0xFF, // 010 LOAD [$variable0] C
            0x00, // 011 (0)
            0x37, // 012 JUMP_IF_LT_ACC #85 @label1
            0x55, // 013 (85)
            0x00  // 014 (0)
        };

        extern const byte num_fibonacci_variable_bytes = 3;

        // Needs to be at least 1 byte in this array
        extern const byte fibonacci_variable_bytes[] PROGMEM = {
            0x7B, // 000 $variable0
            0xD3, // 001 $variable1
            0x2A  // 002 $variable2
        };

        // Max of seven characters
        extern const char fibonacci_program_name[] = "fibonac";
        """
    )

    assert export.gen_arduino_program_cpp_file(
        assembly_line_infos, "fibonacci", "prog_fibonacci.h") == expected


def test_extract_program_file_machinecode_info(assembly_line_infos):
    expected = [
        {
            "bitstring" : "11111111",
            "comment" : "// 000 LOAD [$variable0] A (@label1)" 
        },
        {
            "bitstring" : "00000000",
            "comment" : "// 001 (0)"
        },
        {
            "bitstring" : "11111111",
            "comment" : "// 002 LOAD [$variable1] A (@label2)"
        },
        {
            "bitstring" : "00000001",
            "comment" : "// 003 (1)"
        },


        {
            "bitstring" : "11111111",
            "comment" : "// 004 JUMP @label1"
        },
        {
            "bitstring" : "00000000",
            "comment" : "// 005 (0)"
        },
        {
            "bitstring" : "11111111",
            "comment" : "// 006 STORE A [#123]"
        },
        {
            "bitstring" : "01111011",
            "comment" : "// 007 (123)"
        },


        {
            "bitstring" : "11111111",
            "comment" : "// 008 LOAD [$variable2] B (@label3)"
        },
        {
            "bitstring" : "00000010",
            "comment" : "// 009 (2)"
        },
        {
            "bitstring" : "11111111",
            "comment" : "// 010 LOAD [$variable0] C"
        },
        {
            "bitstring" : "00000000",
            "comment" : "// 011 (0)"
        },


        {
            "bitstring" : "00110111",
            "comment" : "// 012 JUMP_IF_LT_ACC #85 @label1"
        },
        {
            "bitstring" : "01010101",
            "comment" : "// 013 (85)"
        },
        {
            "bitstring" : "00000000",
            "comment" : "// 014 (0)"
        },
    ]

    assert export.extract_program_file_machinecode_info(assembly_line_infos) == expected

def test_extract_program_file_variable_info(assembly_line_infos):
    expected = [
        {
            "value" : 123,
            "name" : "$variable0"
        },
        {
            "value" : -45,
            "name" : "$variable1"
        },
        {
            "value" : 42,
            "name" : "$variable2"
        },
    ]

    assert export.extract_program_file_variable_info(assembly_line_infos) == expected

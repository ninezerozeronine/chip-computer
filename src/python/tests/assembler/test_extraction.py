import textwrap

import pytest

from eight_bit_computer.assembler import extraction


def test_get_assembly_summary_data(assembly_line_infos, assembly_summary_data):
    assert extraction.get_assembly_summary_data(assembly_line_infos) == assembly_summary_data


def test_generate_assembly_summary_lines(assembly_line_infos):
    expected = [
        " 1 $variable0              |",
        " 2 @label1                 |",
        " 3     LOAD [$variable1] A |  0 00 00000000 - @label1 255 FF 11111111",
        "                           |  1 01 00000001 -           1 01 00000001 $variable1",
        " 4                         |",
        " 5 @label2                 |",
        " 6     LOAD [$variable2] A |  2 02 00000010 - @label2 255 FF 11111111",
        "                           |  3 03 00000011 -           2 02 00000010 $variable2",
        " 7     JUMP @label1        |  4 04 00000100 -         255 FF 11111111",
        "                           |  5 05 00000101 -           0 00 00000000 @label1",
        " 8                         |",
        " 9     STORE A [#123]      |  6 06 00000110 -         255 FF 11111111",
        "                           |  7 07 00000111 -         123 7B 01111011 #123",
        "10 @label3                 |",
        "11     LOAD [$variable3] B |  8 08 00001000 - @label3 255 FF 11111111",
        "                           |  9 09 00001001 -           3 03 00000011 $variable3",
        "12     LOAD [$variable0] C | 10 0A 00001010 -         255 FF 11111111",
        "                           | 11 0B 00001011 -           0 00 00000000 $variable0",
        "13 $variable4              |",
        "14 // comment              |",
    ]
    assert extraction.generate_assembly_summary_lines(assembly_line_infos) == expected


def test_get_widest_column_values(assembly_summary_data):
    expected = {
        "asm_line_no": 2,
        "asm_line": 23,
        "mc_index_decimal": 2,
        "mc_byte_decimal": 3,
        "mc_label": 7,
    }
    assert extraction.get_widest_column_values(assembly_summary_data) == expected

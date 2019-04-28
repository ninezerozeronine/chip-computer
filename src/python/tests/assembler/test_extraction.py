import textwrap

import pytest

from eight_bit_computer.assembler import extraction


def test_get_assembly_summary_data(assembly_line_infos, assembly_summary_data):
    assert extraction.get_assembly_summary_data(assembly_line_infos) == assembly_summary_data


def test_generate_assembly_summary(assembly_line_infos):
    expected = textwrap.dedent(
        """\
         1 $variable0              |
         2 @label1                 |
         3     LOAD [$variable1] A |  0 00 00000000 - @label1 11111111 FF
                                   |  1 01 00000001 -         00000001 01 $variable1
         4                         |
         5 @label2                 |
         6     LOAD [$variable2] A |  2 02 00000010 - @label2 11111111 FF
                                   |  3 03 00000011 -         00000010 02 $variable2
         7     JUMP @label1        |  4 04 00000100 -         11111111 FF
                                   |  5 05 00000101 -         00000000 00 @label1
         8                         |
         9     STORE A [#123]      |  6 06 00000110 -         11111111 FF
                                   |  7 07 00000111 -         01111011 7B #123
        10 @label3                 |
        11     LOAD [$variable3] B |  8 08 00001000 - @label3 11111111 FF
                                   |  9 09 00001001 -         00000011 03 $variable3
        12     LOAD [$variable0] C | 10 0A 00001010 -         11111111 FF
                                   | 11 0B 00001011 -         00000000 00 $variable0
        13 $variable4              |
        14 // comment              |"""
    )
    assert extraction.generate_assembly_summary(assembly_line_infos) == expected


def test_get_widest_column_values(assembly_summary_data):
    expected = {
        "asm_line_no": 2,
        "asm_line": 23,
        "mc_index_decimal": 2,
        "mc_label": 7,
    }
    assert extraction.get_widest_column_values(assembly_summary_data) == expected

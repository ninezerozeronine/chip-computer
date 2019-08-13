import textwrap

import pytest

from eight_bit_computer import export


def test_bitstrings_to_arduino_cpp():
    test_data = [
        "10111110", "11101111", "11111010", "11001110",    "10111110", "11101111", "11111010", "11001110",    "10111110", "11101111", "11111010", "11001110",    "10111110", "11101111", "11111010", "11001110",
        "00000000", "11111111", "10101010", "01010101",    "10111110", "11101111", "11111010", "11001110",    "10111110", "11101111", "11111010", "11001110",    "10111110", "11101111", "11111010", "11001110",
    ]
    expected = textwrap.dedent(
        """\
        #include "rom_0.h"

        extern const byte ROM_0[] __attribute__ (( __section__(".fini1") )) = {
            0xBE, 0xEF, 0xFA, 0xCE,  0xBE, 0xEF, 0xFA, 0xCE,  0xBE, 0xEF, 0xFA, 0xCE,  0xBE, 0xEF, 0xFA, 0xCE, // 00000
            0x00, 0xFF, 0xAA, 0x55,  0xBE, 0xEF, 0xFA, 0xCE,  0xBE, 0xEF, 0xFA, 0xCE,  0xBE, 0xEF, 0xFA        // 00016
        };
        extern const byte ROM_0_last_byte = 0xCE;
        """
    )

    assert export.bitstrings_to_arduino_cpp(0, "rom", test_data) == expected


def test_create_arduino_header():
    expected = textwrap.dedent(
        """\
        #ifndef ROM_0_H
        #define ROM_0_H

        #include <Arduino.h>

        extern const byte ROM_0[];
        extern const byte ROM_0_last_byte;

        #endif
        """
    )

    assert export.create_arduino_header(0, "rom") == expected


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
def test_number_to_bitstring(seq, chunk_size, expected):
    generator = export.chunker(seq, chunk_size)
    generator_tester(generator, expected)

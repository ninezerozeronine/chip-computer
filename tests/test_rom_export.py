import pytest
import textwrap

from sixteen_bit_computer import rom_export

def test_generate_arduino_cpp():
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

    assert rom_export.generate_arduino_cpp(test_data, 0, "example_header.h", "EXAMPLE_VAR_NAME") == expected


def test_generate_arduino_header():
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

    assert rom_export.generate_arduino_header("header_filename", "EXAMPLE_VAR_NAME") == expected


def test_generate_logisim():
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
    assert rom_export.generate_logisim(test_data) == expected

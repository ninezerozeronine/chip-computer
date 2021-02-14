import pytest

from sixteen_bit_computer import language_defs


@pytest.mark.parametrize("test_input,expected", [
    (
        [
            "00011100",
        ],
        "00011100"
    ),
    (
        [
            "0000....",
            "....1111",
        ],
        "00001111"
    ),
    (
        [
            "1100....110....",
            "....0011....01.",
        ],
        "11000011"
    ),
])
def test_instruction_byte_from_bitdefs(test_input, expected):
    assert language_defs.instruction_byte_from_bitdefs(test_input) == expected

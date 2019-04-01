import pytest

from eight_bit_computer.language import definitions

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
    assert definitions.instruction_byte_from_bitdefs(test_input) == expected

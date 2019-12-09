import pytest

from eight_bit_computer import decimal_display
from eight_bit_computer.bitdef import remove_whitespace as rw
from eight_bit_computer.language_defs import DISPLAY_OPTIONS
from eight_bit_computer.data_structures import RomData

@pytest.mark.parametrize("test_input, expected", [
    (1,1),
    (0,0),
    (127, 127),
    (128, -128),
    (213, -43),
    (255, -1),
])
def test_to_2s_compliment(test_input, expected):
    assert decimal_display.to_2s_compliment(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [
    (0,   "000....00000000"),
    (255, "000....11111111"),
    (128, "000....10000000"),
    (85,  "000....01010101"),
    (170, "000....10101010"),
])
def test_value_to_addr_bitdef(test_input, expected):
    assert decimal_display.value_to_addr_bitdef(test_input) == expected

@pytest.mark.parametrize("test_input, expected", [
    ("A", "01110111"),
    ("-", "01000000"),
    ("8", "01111111"),
    (" ", "00000000"),
])
def test_character_to_bitdef(test_input, expected):
    assert decimal_display.character_to_bitdef(test_input) == expected

@pytest.mark.parametrize("test_input", ["Q", ".", "?",])
def test_character_to_bitdef_raises(test_input):
    with pytest.raises(ValueError):
        decimal_display.character_to_bitdef(test_input)

@pytest.mark.parametrize("raw_value, disp_chars, base_bitdef, binary_mode_bitdef, expected", [
    (
        0,
        "   0",
        DISPLAY_OPTIONS["DECIMAL"],
        DISPLAY_OPTIONS["UNSIGNED"],
        [
            RomData(address=rw("000 00 11 0000 0000"), data=rw("0000 0000")),
            RomData(address=rw("000 00 10 0000 0000"), data=rw("0000 0000")),
            RomData(address=rw("000 00 01 0000 0000"), data=rw("0000 0000")),
            RomData(address=rw("000 00 00 0000 0000"), data=rw("0011 1111")),
        ]
    ),
    (
        15,
        "   F",
        DISPLAY_OPTIONS["HEX"],
        DISPLAY_OPTIONS["TWOS_COMP"],
        [
            RomData(address=rw("000 11 11 0000 1111"), data=rw("0000 0000")),
            RomData(address=rw("000 11 10 0000 1111"), data=rw("0000 0000")),
            RomData(address=rw("000 11 01 0000 1111"), data=rw("0000 0000")),
            RomData(address=rw("000 11 00 0000 1111"), data=rw("0111 0001")),
        ]
    ),
    (
        200,
        " -56",
        DISPLAY_OPTIONS["DECIMAL"],
        DISPLAY_OPTIONS["TWOS_COMP"],
        [
            RomData(address=rw("000 10 11 1100 1000"), data=rw("0000 0000")),
            RomData(address=rw("000 10 10 1100 1000"), data=rw("0100 0000")),
            RomData(address=rw("000 10 01 1100 1000"), data=rw("0110 1101")),
            RomData(address=rw("000 10 00 1100 1000"), data=rw("0111 1101")),
        ]
    ),
])
def test_assemble_romdata(raw_value, disp_chars, base_bitdef, binary_mode_bitdef, expected):
    assert decimal_display.assemble_romdata(
        raw_value, disp_chars, base_bitdef, binary_mode_bitdef) == expected


def test_gen_display_romdatas_doesnt_raise():
    decimal_display.gen_display_romdatas()
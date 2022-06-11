import pytest

from sixteen_bit_computer import microcode_rom
from sixteen_bit_computer.data_structures import DataTemplate, RomData


@pytest.mark.slow
def test_get_rom_doesnt_raise():
    data = microcode_rom.get_rom()
    assert True


@pytest.mark.parametrize("test_input,expected", [
    (
        [
            DataTemplate(address_range="00.", data="00"),
        ],
        [
            RomData(address="000", data="00"),
            RomData(address="001", data="00"),
        ],
    ),
    (
        [
            DataTemplate(address_range=".", data="10"),
        ],
        [
            RomData(address="0", data="10"),
            RomData(address="1", data="10"),
        ],
    ),
    (
        [
            DataTemplate(address_range="0", data="10"),
        ],
        [
            RomData(address="0", data="10"),
        ],
    ),
    (
        [
            DataTemplate(address_range="01.", data="0"),
            DataTemplate(address_range="10.", data="1"),
        ],
        [
            RomData(address="010", data="0"),
            RomData(address="011", data="0"),
            RomData(address="100", data="1"),
            RomData(address="101", data="1"),
        ],
    ),
    (
        [
            DataTemplate(address_range="0..", data="0"),
            DataTemplate(address_range="11.", data="1"),
        ],
        [
            RomData(address="000", data="0"),
            RomData(address="001", data="0"),
            RomData(address="010", data="0"),
            RomData(address="011", data="0"),
            RomData(address="110", data="1"),
            RomData(address="111", data="1"),
        ],
    ),
])
def test_collapse_datatemplates_to_romdatas(test_input, expected):
    assert microcode_rom.collapse_datatemplates_to_romdatas(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    (
        [
            RomData(
                address="0",
                data="10101010111111110000000011001100"
            ),
            RomData(
                address="1",
                data="00000000110000110011110011110000"
            ),
        ],
        {
            0: [
                    RomData(address="0", data="11001100"),
                    RomData(address="1", data="11110000"),
            ],
            1: [
                    RomData(address="0", data="00000000"),
                    RomData(address="1", data="00111100"),
            ],
            2: [
                    RomData(address="0", data="11111111"),
                    RomData(address="1", data="11000011"),
            ],
            3:  [
                    RomData(address="0", data="10101010"),
                    RomData(address="1", data="00000000"),
            ],
        }
    ),
    (
        [
            RomData(
                address="0",
                data="1010101011111111"
            ),
        ],
        {
            0: [
                    RomData(address="0", data="11111111"),
            ],
            1: [
                    RomData(address="0", data="10101010"),
            ],
        }
    ),
])
def test_slice_rom(test_input, expected):
    assert microcode_rom.slice_rom(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    ("010", 1),
    ("01001111", 1),
    ("010011110", 2),
    ("00000000111111110000000011111111", 4),
])
def test_get_num_bytes(test_input, expected):
    assert microcode_rom.get_num_bytes(test_input) == expected


@pytest.mark.parametrize("romdatas,end,start,expected", [
    (
        [
            RomData(address="00", data="0000"),
            RomData(address="11", data="1101"),
        ],
        2,
        0,
        [
            RomData(address="00", data="000"),
            RomData(address="11", data="101"),
        ]
    ),
    (
        [
            RomData(address="00", data="0000"),
            RomData(address="11", data="1101"),
        ],
        0,
        0,
        [
            RomData(address="00", data="0"),
            RomData(address="11", data="1"),
        ]
    ),
])
def test_get_romdata_slice(romdatas, end, start, expected):
    assert microcode_rom.get_romdata_slice(romdatas, end, start) == expected



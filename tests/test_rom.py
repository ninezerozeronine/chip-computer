import pytest

from eight_bit_computer import rom
from eight_bit_computer.data_structures import DataTemplate


@pytest.mark.slow
def test_get_rom_doesnt_raise():
    data = rom.get_rom()
    assert True


@pytest.mark.parametrize("test_input,expected", [
    (
        [
            DataTemplate(address_range="00.", data="00"),
        ],
        [
            rom.RomData(address="000", data="00"),
            rom.RomData(address="001", data="00"),
        ],
    ),
    (
        [
            DataTemplate(address_range=".", data="10"),
        ],
        [
            rom.RomData(address="0", data="10"),
            rom.RomData(address="1", data="10"),
        ],
    ),
    (
        [
            DataTemplate(address_range="0", data="10"),
        ],
        [
            rom.RomData(address="0", data="10"),
        ],
    ),
    (
        [
            DataTemplate(address_range="01.", data="0"),
            DataTemplate(address_range="10.", data="1"),
        ],
        [
            rom.RomData(address="010", data="0"),
            rom.RomData(address="011", data="0"),
            rom.RomData(address="100", data="1"),
            rom.RomData(address="101", data="1"),
        ],
    ),
    (
        [
            DataTemplate(address_range="0..", data="0"),
            DataTemplate(address_range="11.", data="1"),
        ],
        [
            rom.RomData(address="000", data="0"),
            rom.RomData(address="001", data="0"),
            rom.RomData(address="010", data="0"),
            rom.RomData(address="011", data="0"),
            rom.RomData(address="110", data="1"),
            rom.RomData(address="111", data="1"),
        ],
    ),
])
def test_collapse_datatemplates_to_romdatas(test_input, expected):
    assert rom.collapse_datatemplates_to_romdatas(test_input) == expected


@pytest.mark.parametrize("romdatas,all_addresses,default_data,expected", [
    (
        [
            rom.RomData(address="00", data="0000"),
            rom.RomData(address="11", data="1111"),
        ],
        [
            '00',
            '01',
            '10',
            '11',
        ],
        "0101",
        [
            rom.RomData(address="00", data="0000"),
            rom.RomData(address="01", data="0101"),
            rom.RomData(address="10", data="0101"),
            rom.RomData(address="11", data="1111"),
        ]
    )
])
def test_populate_empty_addresses(romdatas, all_addresses, default_data, expected):
    assert rom.populate_empty_addresses(romdatas, all_addresses, default_data) == expected


@pytest.mark.parametrize("test_input,expected", [
    (
        [
            rom.RomData(address="00", data="0000"),
            rom.RomData(address="00", data="0000"),
            rom.RomData(address="11", data="0000"),
        ],
        True
    ),
    (
        [
            rom.RomData(address="00", data="0000"),
            rom.RomData(address="01", data="0000"),
            rom.RomData(address="11", data="0000"),
        ],
        False
    )
])
def test_romdatas_have_duplicate_addresses(test_input, expected):
    assert rom.romdatas_have_duplicate_addresses(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    (
        [
            "10101010111111110000000011001100",
            "00000000110000110011110011110000",
        ],
        {
            0: [
                    "11001100",
                    "11110000",
            ],
            1: [
                    "00000000",
                    "00111100",
            ],
            2: [
                    "11111111",
                    "11000011",
            ],
            3:  [
                    "10101010",
                    "00000000",
            ],
        }
    ),
    (
        [
            "1010101011111111",
        ],
        {
            0: [
                    "11111111",
            ],
            1: [
                    "10101010",
            ],
        }
    ),
])
def test_slice_rom(test_input, expected):
    assert rom.slice_rom(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    ("010", 1),
    ("01001111", 1),
    ("010011110", 2),
    ("00000000111111110000000011111111", 4),
])
def test_get_num_bytes(test_input, expected):
    assert rom.get_num_bytes(test_input) == expected


@pytest.mark.parametrize("romdatas,end,start,expected", [
    (
        [
            "0000",
            "1101",
        ],
        2,
        0,
        [
            "000",
            "101",
        ]
    ),
    (
        [
            "0000",
            "1101",
        ],
        0,
        0,
        [
            "0",
            "1",
        ]
    ),
])
def test_get_rom_slice(romdatas, end, start, expected):
    assert rom.get_rom_slice(romdatas, end, start) == expected

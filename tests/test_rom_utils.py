import pytest

from sixteen_bit_computer import rom_utils
from sixteen_bit_computer.data_structures import RomData

@pytest.mark.parametrize("romdatas,all_addresses,default_data,expected", [
    (
        [
            RomData(address="00", data="0000"),
            RomData(address="11", data="1111"),
        ],
        [
            '00',
            '01',
            '10',
            '11',
        ],
        "0101",
        [
            RomData(address="00", data="0000"),
            RomData(address="01", data="0101"),
            RomData(address="10", data="0101"),
            RomData(address="11", data="1111"),
        ]
    )
])
def test_populate_empty_addresses(romdatas, all_addresses, default_data, expected):
    assert rom_utils.populate_empty_addresses(romdatas, all_addresses, default_data) == expected


@pytest.mark.parametrize("test_input,expected", [
    (
        [
            RomData(address="00", data="0000"),
            RomData(address="00", data="0000"),
            RomData(address="11", data="0000"),
        ],
        True
    ),
    (
        [
            RomData(address="00", data="0000"),
            RomData(address="01", data="0000"),
            RomData(address="11", data="0000"),
        ],
        False
    )
])
def test_romdatas_have_duplicate_addresses(test_input, expected):
    assert rom_utils.romdatas_have_duplicate_addresses(test_input) == expected

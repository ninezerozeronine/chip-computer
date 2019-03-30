import pytest

from eight_bit_computer import rom
from eight_bit_computer.datatemplate import DataTemplate


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

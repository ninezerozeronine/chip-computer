import unittest

from eight_bit_computer import rom
from eight_bit_computer.datatemplate import DataTemplate


class TestRom(unittest.TestCase):

    def test_collapse_datatemplates_to_romdatas(self):
        test_data = [
            {
                "datatemplates": [
                    DataTemplate(address_range="00.", data="00"),
                ],
                "romdatas": [
                    rom.RomData(address="000", data="00"),
                    rom.RomData(address="001", data="00"),
                ]
            },
            {
                "datatemplates": [
                    DataTemplate(address_range=".", data="10"),
                ],
                "romdatas": [
                    rom.RomData(address="0", data="10"),
                    rom.RomData(address="1", data="10"),
                ]
            },
            {
                "datatemplates": [
                    DataTemplate(address_range="0", data="10"),
                ],
                "romdatas": [
                    rom.RomData(address="0", data="10"),
                ]
            },
            {
                "datatemplates": [
                    DataTemplate(address_range="01.", data="0"),
                    DataTemplate(address_range="10.", data="1"),
                ],
                "romdatas": [
                    rom.RomData(address="010", data="0"),
                    rom.RomData(address="011", data="0"),
                    rom.RomData(address="100", data="1"),
                    rom.RomData(address="101", data="1"),
                ]
            },
            {
                "datatemplates": [
                    DataTemplate(address_range="0..", data="0"),
                    DataTemplate(address_range="11.", data="1"),
                ],
                "romdatas": [
                    rom.RomData(address="000", data="0"),
                    rom.RomData(address="001", data="0"),
                    rom.RomData(address="010", data="0"),
                    rom.RomData(address="011", data="0"),
                    rom.RomData(address="110", data="1"),
                    rom.RomData(address="111", data="1"),
                ]
            },
        ]

        for test_set in test_data:
            self.assertEqual(
                rom.collapse_datatemplates_to_romdatas(test_set["datatemplates"]),
                test_set["romdatas"],
            )

    def test_get_romdata_slice(self):
        pass

import unittest

from eight_bit_computer import bitdef, rom, utils


class TestBitdef(unittest.TestCase):

    def test_same_length(self):
        true_tests = [
            [
                ".",
                "0",
                "1",
            ],
            [
                "...",
                "0.1",
                "1..",
            ],
            [
                "",
                "",
            ]
        ]

        for bitdefs in true_tests:
            self.assertTrue(bitdef.same_length(bitdefs))

        false_tests = [
            [
                "..",
                "0",
                "1111",
            ],
            [
                "...",
                "0.1",
                "1...",
            ],
            [
                "...",
                "0.1",
                "",
            ],
        ]

        for bitdefs in false_tests:
            self.assertFalse(bitdef.same_length(bitdefs))

    def test_length(self):
        test_data = [
            ("00010", 5),
            ("", 0),
            (".", 1),
            ("01.100", 6),
        ]

        for test_bitdef, length in test_data:
            self.assertEqual(bitdef.length(test_bitdef), length)

    def test_have_overlapping_bits(self):
        true_tests = [
            [
                "0",
                "0",
            ],
            [
                "0.",
                "1.",
            ],
            [
                "..0.",
                "1.1.",
            ],
            [
                "....0.",
                "....1.",
            ],
            [
                "......",
                "....0.",
                "....1.",
            ],
        ]

        for bitdefs in true_tests:
            self.assertTrue(bitdef.have_overlapping_bits(bitdefs))

        false_tests = [
            [
                "",
            ],
            [
                "",
                "",
                "",
            ],
            [
                ".",
                "1",
                ".",
            ],
            [
                "...0.",
                "1....",
                "..1..",
            ],
            [
                "...",
                "...",
                "...",
            ],
        ]

        for bitdefs in false_tests:
            self.assertFalse(bitdef.have_overlapping_bits(bitdefs))

        raises_tests = [
            [
                ".10",
                "010.",
            ],
            [
                ".",
                "",
            ],
        ]

        for bitdefs in raises_tests:
            with self.assertRaises(ValueError):
                bitdef.have_overlapping_bits(bitdefs)

    def test_merge(self):
        test_data = [
            {
                "bitdefs": [
                    "",
                ],
                "result":
                    "",
            },
            {
                "bitdefs": [
                    ".",
                ],
                "result":
                    ".",
            },
            {
                "bitdefs": [
                    "0",
                ],
                "result":
                    "0",
            },
            {
                "bitdefs": [
                    "1",
                ],
                "result":
                    "1",
            },
            {
                "bitdefs": [
                    "0...",
                    ".1..",
                    "..0.",
                ],
                "result":
                    "010.",
            },
        ]

        for test_set in test_data:
            self.assertEqual(bitdef.merge(test_set["bitdefs"]), test_set["result"])

        raises_tests = [
            [
                "0",
                "1",
            ],
            [
                "..0",
                "..1",
            ],
            [
                "00",
                "1",
            ],
        ]

        for bitdefs in raises_tests:
            with self.assertRaises(ValueError):
                bitdef.merge(bitdefs)

    def test_collapse(self):
        test_data = [
            {
                "bitdef": "",
                "result": [
                    "",
                ]
            },
            {
                "bitdef": ".",
                "result": [
                    "0",
                    "1"
                ]
            },
            {
                "bitdef": "..",
                "result": [
                    "00",
                    "01",
                    "10",
                    "11",
                ]
            },
            {
                "bitdef": "1..0",
                "result": [
                    "1000",
                    "1010",
                    "1100",
                    "1110",
                ]
            }
        ]

        for test_set in test_data:
            self.assertEqual(
                bitdef.collapse(test_set["bitdef"]), test_set["result"]
            )

    def test_fill_bitdef(self):
        test_data = [
            ("", "", "1"),
            (".", "0", "0"),
            (".10.", "1101", "1"),
            ("1010", "1010", "0"),
        ]

        for test_bitdef, result, fill_value in test_data:
            self.assertEqual(bitdef.fill(test_bitdef, fill_value), result)

    def test_extract_bits(self):
        test_data = [
            {
                "bitdef": "001010.",
                "start": 0,
                "end": 6,
                "result": "001010.",
            },
            {
                "bitdef": "11..11",
                "start": 3,
                "end": 5,
                "result": "11.",
            },
            {
                "bitdef": "..01.010",
                "start": 1,
                "end": 1,
                "result": "1",
            },
        ]

        for test_set in test_data:
            self.assertEqual(
                bitdef.extract_bits(
                    test_set["bitdef"], test_set["end"], test_set["start"]
                ),
                test_set["result"],
            )

    def test_remove_whitespace(self):
        test_data = [
            ("", ""),
            ("0", "0"),
            ("00 01", "0001"),
            ("  ..  00  1  ", "..001"),
        ]

        for test, result in test_data:
            self.assertEqual(bitdef.remove_whitespace(test), result)

    def test_reverse_index(self):
        test_data = [
            {
                "index": 0,
                "length": 6,
                "result": 5,
            },
            {
                "index": 0,
                "length": 1,
                "result": 0,
            },
            {
                "index": 1,
                "length": 4,
                "result": 2,
            },
            {
                "index": 3,
                "length": 4,
                "result": 0,
            },
        ]

        for test_set in test_data:
            self.assertEqual(
                bitdef.reverse_index(test_set["index"], test_set["length"]),
                test_set["result"]
            )


class TestRom(unittest.TestCase):

    def test_collapse_datatemplates_to_romdatas(self):
        test_data = [
            {
                "datatemplates": [
                    utils.DataTemplate(address_range="00.", data="00"),
                ],
                "romdatas": [
                    rom.RomData(address="000", data="00"),
                    rom.RomData(address="001", data="00"),
                ]
            },
            {
                "datatemplates": [
                    utils.DataTemplate(address_range=".", data="10"),
                ],
                "romdatas": [
                    rom.RomData(address="0", data="10"),
                    rom.RomData(address="1", data="10"),
                ]
            },
            {
                "datatemplates": [
                    utils.DataTemplate(address_range="0", data="10"),
                ],
                "romdatas": [
                    rom.RomData(address="0", data="10"),
                ]
            },
            {
                "datatemplates": [
                    utils.DataTemplate(address_range="01.", data="0"),
                    utils.DataTemplate(address_range="10.", data="1"),
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
                    utils.DataTemplate(address_range="0..", data="0"),
                    utils.DataTemplate(address_range="11.", data="1"),
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


if __name__ == '__main__':
    unittest.main()

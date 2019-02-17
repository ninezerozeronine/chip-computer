import unittest

from eight_bit_computer import utils

class TestUtils(unittest.TestCase):

    def test_bitdefs_same_length(self):
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
            self.assertTrue(utils.bitdefs_same_length(bitdefs))


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
            self.assertFalse(utils.bitdefs_same_length(bitdefs))


    def test_bitdef_length(self):
        test_data = [
            ("00010", 5),
            ("", 0),
            (".", 1),
            ("01.100", 6),
        ]

        for bitdef, length in test_data:
            self.assertEqual(utils.bitdef_length(bitdef), length)


    def test_bitdefs_have_overlapping_bits(self):
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
            self.assertTrue(utils.bitdefs_have_overlapping_bits(bitdefs))

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
            self.assertFalse(utils.bitdefs_have_overlapping_bits(bitdefs))

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
                utils.bitdefs_have_overlapping_bits(bitdefs)

    def test_remove_whitespace(self):
        test_data = [
            ("", ""),
            ("0", "0"),
            ("00 01", "0001"),
            ("  ..  00  1  ", "..001"),
        ]

        for test, result in test_data:
            self.assertEqual(utils.remove_whitespace(test), result)

    def test_merge_bitdefs(self):
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
            self.assertEqual(utils.merge_bitdefs(test_set["bitdefs"]), test_set["result"])

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
                utils.merge_bitdefs(bitdefs)

    def test_collapse_bitdef(self):
        test_data = [
            {
                "bitdef": "",
                "result": set([
                    "",
                ])
            },
            {
                "bitdef": ".",
                "result": set([
                    "0",
                    "1"
                ])
            },
            {
                "bitdef": "..",
                "result": set([
                    "00",
                    "01",
                    "10",
                    "11",
                ])
            },
            {
                "bitdef": "1..0",
                "result": set([
                    "1000",
                    "1010",
                    "1100",
                    "1110",
                ])
            }
        ]

        for test_set in test_data:
            self.assertEqual(
                set(utils.collapse_bitdef(test_set["bitdef"])), test_set["result"]
            )

    def test_fill_bitdef(self):
        test_data = [
            ("", "", "1"),
            (".", "0", "0"),
            (".10.", "1101", "1"),
            ("1010", "1010", "0"),
        ]

        for bitdef, result, fill_value in test_data:
            self.assertEqual(utils.fill_bitdef(bitdef, fill_value), result)


    def test_datatemplates_to_romdatas(self):
        test_data = [
            {
                "datatemplates": [
                    utils.DataTemplate(address_range="00.", data="00"),
                ],
                "romdatas": [
                    utils.RomData(address="000", data="00"),
                    utils.RomData(address="001", data="00"),
                ]
            },
            {
                "datatemplates": [
                    utils.DataTemplate(address_range=".", data="10"),
                ],
                "romdatas": [
                    utils.RomData(address="0", data="10"),
                    utils.RomData(address="1", data="10"),
                ]
            },
            {
                "datatemplates": [
                    utils.DataTemplate(address_range="0", data="10"),
                ],
                "romdatas": [
                    utils.RomData(address="0", data="10"),
                ]
            },
            {
                "datatemplates": [
                    utils.DataTemplate(address_range="01.", data="0"),
                    utils.DataTemplate(address_range="10.", data="1"),
                ],
                "romdatas": [
                    utils.RomData(address="010", data="0"),
                    utils.RomData(address="011", data="0"),
                    utils.RomData(address="100", data="1"),
                    utils.RomData(address="101", data="1"),
                ]
            },
            {
                "datatemplates": [
                    utils.DataTemplate(address_range="10.", data="0"),
                    utils.DataTemplate(address_range="10.", data="1"),
                ],
                "romdatas": [
                    utils.RomData(address="100", data="0"),
                    utils.RomData(address="101", data="0"),
                    utils.RomData(address="100", data="1"),
                    utils.RomData(address="101", data="1"),
                ]
            },
        ]

        for test_set in test_data:
            self.assertEqual(
                utils.datatemplates_to_romdatas(test_set["datatemplates"]),
                test_set["romdatas"],
            )


if __name__ == '__main__':
    unittest.main()
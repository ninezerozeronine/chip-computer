import unittest

import utils

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

def test_collapse_bitdef(bitdef):
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
                set(collapse_bitdef(test_set["bitdef"]), test_set["result"])
            )

    # def test_bitdef_limits(self):
    #     bitdefs = [
    #         utils.BitDef(end=3, start=0, value="101X"),
    #         utils.BitDef(end=7, start=4, value="0000")
    #     ]
    #     self.assertEqual(utils.bitdef_limits(bitdefs), (7,0))


    # def test_bitdefs_overlap(self):
    #     non_overlap_bitdefs = [
    #         utils.BitDef(end=3, start=0, value="101X"),
    #         utils.BitDef(end=7, start=4, value="0000")
    #     ]

    #     self.assertFalse(utils.bitdefs_overlap(non_overlap_bitdefs))

    #     overlap_bitdefs = [
    #         utils.BitDef(end=3, start=0, value="1111"),
    #         utils.BitDef(end=7, start=2, value="000000")
    #     ]
    #     self.assertTrue(utils.bitdefs_overlap(overlap_bitdefs))


    # def test_bitdefs_have_gaps(self):
    #     non_gap_bitdefs = [
    #         utils.BitDef(end=3, start=2, value="00"),
    #         utils.BitDef(end=5, start=4, value="11"),
    #         utils.BitDef(end=7, start=6, value="XX")
    #     ]

    #     self.assertFalse(utils.bitdefs_have_gaps(non_gap_bitdefs))

    #     gap_bitdefs = [
    #         utils.BitDef(end=2, start=0, value="111"),
    #         utils.BitDef(end=7, start=4, value="0000")
    #     ]

    #     self.assertTrue(utils.bitdefs_have_gaps(gap_bitdefs))


    # def test_join_bitdefs(self):
    #     bitdefs = [
    #         utils.BitDef(end=3, start=2, value="00"),
    #         utils.BitDef(end=5, start=4, value="11"),
    #         utils.BitDef(end=7, start=6, value="XX")
    #     ]

    #     self.assertEqual(
    #         utils.join_bitdefs(bitdefs),
    #         utils.BitDef(end=7, start=2, value="XX1100")
    #     )

    # def test_resize_bitdef(self):
    #     orig = utils.BitDef(end=2, start=0, value="01X")
    #     new = utils.BitDef(end=2, start=0, value="01X")
    #     self.assertEqual(
    #         new,
    #         utils.resize_bitdef(orig, 2, 0, fill_value="X")
    #     )

    #     orig = utils.BitDef(end=2, start=0, value="01X")
    #     new = utils.BitDef(end=4, start=3, value="11")
    #     self.assertEqual(
    #         new,
    #         utils.resize_bitdef(orig, 4, 3, fill_value="1")
    #     )

    #     orig = utils.BitDef(end=3, start=2, value="01")
    #     new = utils.BitDef(end=1, start=0, value="XX")
    #     self.assertEqual(
    #         new,
    #         utils.resize_bitdef(orig, 1, 0, fill_value="X")
    #     )

    #     orig = utils.BitDef(end=3, start=0, value="101X")
    #     new = utils.BitDef(end=5, start=2, value="XX10")
    #     self.assertEqual(
    #         new,
    #         utils.resize_bitdef(orig, 5, 2, fill_value="X")
    #     )


    # def test_bitdefs_have_different_absolutes(self):
    #     non_overlapping_tests = [
    #         [
    #             utils.BitDef(end=3, start=0, value="1XXX"),
    #             utils.BitDef(end=3, start=0, value="X0XX"),
    #             utils.BitDef(end=3, start=0, value="XX1X"),
    #         ],
    #         [
    #             utils.BitDef(end=3, start=0, value="1XXX"),
    #             utils.BitDef(end=4, start=4, value="1"),
    #         ],
    #         [
    #             utils.BitDef(end=1, start=0, value="XX"),
    #             utils.BitDef(end=1, start=0, value="11"),
    #         ],
    #         [
    #             utils.BitDef(end=1, start=0, value="1X"),
    #             utils.BitDef(end=1, start=0, value="11"),
    #         ],
    #         [
    #             utils.BitDef(end=1, start=0, value="1X"),
    #             utils.BitDef(end=1, start=0, value="X0"),
    #         ],
    #     ]

    #     for non_overlapping in non_overlapping_tests:
    #         self.assertFalse(
    #             utils.bitdefs_have_different_absolutes(non_overlapping)
    #         )

    #     overlapping_tests = [
    #         [
    #             utils.BitDef(end=1, start=0, value="1X"),
    #             utils.BitDef(end=1, start=0, value="00"),
    #         ],
    #         [
    #             utils.BitDef(end=2, start=0, value="1XX"),
    #             utils.BitDef(end=4, start=2, value="XX0"),
    #         ],
    #         [
    #             utils.BitDef(end=3, start=0, value="1100"),
    #             utils.BitDef(end=3, start=0, value="1010"),
    #         ],
    #     ]

    #     for overlapping in overlapping_tests:
    #         self.assertTrue(
    #             utils.bitdefs_have_different_absolutes(overlapping)
    #         )

if __name__ == '__main__':
    unittest.main()
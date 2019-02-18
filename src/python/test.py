import unittest

import utils

class TestUtils(unittest.TestCase):

    def test_bitdef_limits(self):
        bitdefs = [
            utils.BitDef(end=3, start=0, value="101X"),
            utils.BitDef(end=7, start=4, value="0000")
        ]
        self.assertEqual(utils.bitdef_limits(bitdefs), (7,0))


    def test_bitdefs_overlap(self):
        non_overlap_bitdefs = [
            utils.BitDef(end=3, start=0, value="101X"),
            utils.BitDef(end=7, start=4, value="0000")
        ]

        self.assertFalse(utils.bitdefs_overlap(non_overlap_bitdefs))

        overlap_bitdefs = [
            utils.BitDef(end=3, start=0, value="1111"),
            utils.BitDef(end=7, start=2, value="000000")
        ]
        self.assertTrue(utils.bitdefs_overlap(overlap_bitdefs))


    def test_bitdefs_have_gaps(self):
        non_gap_bitdefs = [
            utils.BitDef(end=3, start=2, value="00"),
            utils.BitDef(end=5, start=4, value="11"),
            utils.BitDef(end=7, start=6, value="XX")
        ]

        self.assertFalse(utils.bitdefs_have_gaps(non_gap_bitdefs))

        gap_bitdefs = [
            utils.BitDef(end=2, start=0, value="111"),
            utils.BitDef(end=7, start=4, value="0000")
        ]

        self.assertTrue(utils.bitdefs_have_gaps(gap_bitdefs))


    def test_join_bitdefs(self):
        bitdefs = [
            utils.BitDef(end=3, start=2, value="00"),
            utils.BitDef(end=5, start=4, value="11"),
            utils.BitDef(end=7, start=6, value="XX")
        ]

        self.assertEqual(
            utils.join_bitdefs(bitdefs),
            utils.BitDef(end=7, start=2, value="XX1100")
        )

    def test_resize_bitdef(self):
        orig = utils.BitDef(end=2, start=0, value="01X")
        new = utils.BitDef(end=2, start=0, value="01X")
        self.assertEqual(
            new,
            utils.resize_bitdef(orig, 2, 0, fill_value="X")
        )

        orig = utils.BitDef(end=2, start=0, value="01X")
        new = utils.BitDef(end=4, start=3, value="11")
        self.assertEqual(
            new,
            utils.resize_bitdef(orig, 4, 3, fill_value="1")
        )

        orig = utils.BitDef(end=3, start=2, value="01")
        new = utils.BitDef(end=1, start=0, value="XX")
        self.assertEqual(
            new,
            utils.resize_bitdef(orig, 1, 0, fill_value="X")
        )

        orig = utils.BitDef(end=3, start=0, value="101X")
        new = utils.BitDef(end=5, start=2, value="XX10")
        self.assertEqual(
            new,
            utils.resize_bitdef(orig, 5, 2, fill_value="X")
        )


    def test_bitdefs_have_different_absolutes(self):
        non_overlapping_tests = [
            [
                utils.BitDef(end=3, start=0, value="1XXX"),
                utils.BitDef(end=3, start=0, value="X0XX"),
                utils.BitDef(end=3, start=0, value="XX1X"),
            ],
            [
                utils.BitDef(end=3, start=0, value="1XXX"),
                utils.BitDef(end=4, start=4, value="1"),
            ],
            [
                utils.BitDef(end=1, start=0, value="XX"),
                utils.BitDef(end=1, start=0, value="11"),
            ],
            [
                utils.BitDef(end=1, start=0, value="1X"),
                utils.BitDef(end=1, start=0, value="11"),
            ],
            [
                utils.BitDef(end=1, start=0, value="1X"),
                utils.BitDef(end=1, start=0, value="X0"),
            ],
        ]

        for non_overlapping in non_overlapping_tests:
            self.assertFalse(
                utils.bitdefs_have_different_absolutes(non_overlapping)
            )

        overlapping_tests = [
            [
                utils.BitDef(end=1, start=0, value="1X"),
                utils.BitDef(end=1, start=0, value="00"),
            ],
            [
                utils.BitDef(end=2, start=0, value="1XX"),
                utils.BitDef(end=4, start=2, value="XX0"),
            ],
            [
                utils.BitDef(end=3, start=0, value="1100"),
                utils.BitDef(end=3, start=0, value="1010"),
            ],
        ]

        for overlapping in overlapping_tests:
            self.assertTrue(
                utils.bitdefs_have_different_absolutes(overlapping)
            )

if __name__ == '__main__':
    unittest.main()
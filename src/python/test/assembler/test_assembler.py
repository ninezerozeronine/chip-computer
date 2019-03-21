import unittest

from eight_bit_computer.assembler import assembler


class TestAssembler(unittest.TestCase):

    def test_remove_comments(self):
        tests = [
            [
                "",
                "",
            ],
            [
                "//",
                "",
            ],
            [
                "/hello /world!",
                "/hello /world!",
            ],
            [
                "blah blah//",
                "blah blah",
            ],
            [
                "before//after",
                "before",
            ],
            [
                "   before   //after   ",
                "   before   ",
            ],
        ]

        for test in tests:
            self.assertEqual(assembler.remove_comments(test[0]), test[1])

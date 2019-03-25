import unittest

from eight_bit_computer.assembler import assembler
from eight_bit_computer.exceptions import LineProcessingError


class TestAssembler(unittest.TestCase):

    def test_remove_comments(self):
        tests = [
            {
                "input": "",
                "output": "",
            },
            {
                "input": "//",
                "output": "",
            },
            {
                "input": "/hello /world!",
                "output": "/hello /world!",
            },
            {
                "input": "blah blah//",
                "output": "blah blah",
            },
            {
                "input": "before//after",
                "output": "before",
            },
            {
                "input": "   before   //after   ",
                "output": "   before   ",
            },
        ]

        for test in tests:
            self.assertEqual(assembler.remove_comments(test["input"]), test["output"])

    def test_remove_excess_whitespace(self):
        tests = [
            {
                "input": "",
                "output": "",
            },
            {
                "input": "      ",
                "output": "",
            },
            {
                "input": "LOAD [$foo] A",
                "output": "LOAD [$foo] A",
            },
            {
                "input": "     LOAD     [$foo]     A    ",
                "output": "LOAD [$foo] A",
            },
            {
                "input": "\tLOAD\t\t[$foo]     A  \t  ",
                "output": "LOAD [$foo] A",
            },
            {
                "input": "LOAD [  $foo  ] A",
                "output": "LOAD [ $foo ] A",
            },
            {
                "input": "   LOAD [$foo] A",
                "output": "LOAD [$foo] A",
            },
            {
                "input": "LOAD [$foo] A   ",
                "output": "LOAD [$foo] A",
            },
            {
                "input": "SET A #14  ",
                "output": "SET A #14",
            },
        ]
        for test in tests:
            self.assertEqual(assembler.remove_excess_whitespace(
                test["input"]), test["output"]
            )

    def test_is_label(self):
        tests = [
            {
                "input": "",
                "output": False,
            },
            {
                "input": "      ",
                "output": False,
            },
            {
                "input": "LOAD [$foo] A",
                "output": False,
            },
            {
                "input": "@hello",
                "output": True,
            },
            {
                "input": "@hello_123_blah",
                "output": True,
            },
            {
                "input": "@hello  world  ",
                "output": False,
            },
            {
                "input": "@@monkey",
                "output": False,
            },
        ]
        for test in tests:
            self.assertEqual(assembler.is_label(test["input"]), test["output"])

    def test_is_varaible(self):
        tests = [
            {
                "input": "",
                "output": False,
            },
            {
                "input": "      ",
                "output": False,
            },
            {
                "input": "LOAD [$foo] A",
                "output": False,
            },
            {
                "input": "$hello",
                "output": True,
            },
            {
                "input": "$hello_123_blah",
                "output": True,
            },
            {
                "input": "$hello  world  ",
                "output": False,
            },
            {
                "input": "$$monkey",
                "output": False,
            },
        ]
        for test in tests:
            self.assertEqual(assembler.is_variable(
                test["input"]), test["output"]
            )

    def test_machine_code_from_line(self):
        tests = [
            {
                "input": "",
                "output": [],
            },
        ]
        for test in tests:
            self.assertEqual(assembler.machine_code_from_line(
                test["input"]), test["output"]
            )

        raises_tests = [
            "fwgfgwkhgfkwjgfkg"
        ]
        for test in raises_tests:
            with self.assertRaises(LineProcessingError):
                assembler.machine_code_from_line(test)

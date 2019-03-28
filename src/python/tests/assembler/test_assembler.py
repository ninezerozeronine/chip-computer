import pytest

from eight_bit_computer.assembler import assembler
from eight_bit_computer.exceptions import LineProcessingError


@pytest.mark.parametrize("test_input,expected", [
    (
        [
            {
                "machine_code": "01101100",
                "constant": "",
            },
        ],
        [
            {
                "machine_code": "01101100",
                "constant": "",
            },
        ],
    ),
    (
        [
            {
                "machine_code": "",
                "constant": "@label",
            },
        ],
        [
            {
                "machine_code": "",
                "constant": "@label",
                "constant_type": "label",
            },
        ],
    ),
    (
        [
            {
                "machine_code": "",
                "constant": "$variable",
            },
        ],
        [
            {
                "machine_code": "",
                "constant": "$variable",
                "constant_type": "variable",
            },
        ],
    ),
    (
        [
            {
                "machine_code": "",
                "constant": "#123",
            },
        ],
        [
            {
                "machine_code": "",
                "constant": "#123",
                "constant_type": "number",
                "number_value": 123,
            },
        ],
    ),
    (
        [
            {
                "machine_code": "10101010",
                "constant": "",
            },
            {
                "machine_code": "",
                "constant": "@label",
            },
        ],
        [
            {
                "machine_code": "10101010",
                "constant": "",
            },
            {
                "machine_code": "",
                "constant": "@label",
                "constant_type": "label",
            },
        ],
    ),
])
def test_validate_and_identify_constants(test_input, expected):
    assembler.validate_and_identify_constants(test_input)
    assert test_input == expected


@pytest.mark.parametrize('test_input', [
    [
        {
            "machine_code": "01101100",
            "constant": "fwgjfgwjfgkjh",
        },
    ],
    [
        {
            "machine_code": "01101100",
            "constant": "@number$variable#123",
        },
    ],
    [
        {
            "machine_code": "01101100",
            "constant": "#9999",
        },
    ],
])
def test_validate_and_identify_constants_raises(test_input):
    with pytest.raises(LineProcessingError):
        assembler.validate_and_identify_constants(test_input)


@pytest.mark.parametrize("test_input,expected", [
    ("#123", True),
    ("#0xFF", True),
    ("#0o22", True),
    ("#0b101", True),
    ("##", False),
    ("", False),
    ("#0q12", False),
    ("#0b10#g", False),
    ("blah", False),
])
def test_is_number(test_input, expected):
    assert assembler.is_number(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    (["#123", 123]),
    (["#0", 0]),
    (["#-12", -12]),
    (["#0xFF", 255]),
    (["#0xff", 255]),
    (["#0o10", 8]),
    (["#0b101", 5]),
])
def test_number_constant_value(test_input, expected):
    assert assembler.number_constant_value(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    # A simple case with a label and a line under it.
    (
        [
            {
                "line_no": 1,
                "raw": "@label1",
                "clean": "@label1",

                "defined_label": "@label1",
                "assigned_label": "",

                "defined_variable": "",

                "machine_code": [],
            },
            {
                "line_no": 2,
                "raw": "LOAD [$variable] A",
                "clean": "LOAD [$variable] A",

                "defined_label": "",
                "assigned_label": "",

                "defined_variable": "",

                "machine_code": [
                    {
                        "machine_code": "10101010",
                        "constant": "",
                    },
                    {
                        "machine_code": "",
                        "constant": "$variable",
                        "constant_type": "variable",
                    },
                ],
            },
        ],
        [
            {
                "line_no": 1,
                "raw": "@label1",
                "clean": "@label1",

                "defined_label": "@label1",
                "assigned_label": "",

                "defined_variable": "",

                "machine_code": [],
            },
            {
                "line_no": 2,
                "raw": "LOAD [$variable] A",
                "clean": "LOAD [$variable] A",

                "defined_label": "",
                "assigned_label": "@label1",

                "defined_variable": "",

                "machine_code": [
                    {
                        "machine_code": "10101010",
                        "constant": "",
                    },
                    {
                        "machine_code": "",
                        "constant": "$variable",
                        "constant_type": "variable",
                    },
                ],
            },
        ],
    ),
    # A more complicated case with two labels and two lines.
    (
        [
            {
                "line_no": 1,
                "raw": "@label1",
                "clean": "@label1",

                "defined_label": "@label1",
                "assigned_label": "",

                "defined_variable": "",

                "machine_code": [],
            },
            {
                "line_no": 2,
                "raw": "LOAD [$variable] A",
                "clean": "LOAD [$variable] A",

                "defined_label": "",
                "assigned_label": "",

                "defined_variable": "",

                "machine_code": [
                    {
                        "machine_code": "10101010",
                        "constant": "",
                    },
                    {
                        "machine_code": "",
                        "constant": "$variable",
                        "constant_type": "variable",
                    },
                ],
            },
            {
                "line_no": 3,
                "raw": "@label2",
                "clean": "@label2",

                "defined_label": "@label2",
                "assigned_label": "",

                "defined_variable": "",

                "machine_code": [],
            },
            {
                "line_no": 4,
                "raw": "LOAD [$other_variable] A",
                "clean": "LOAD [$other_variable] A",

                "defined_label": "",
                "assigned_label": "",

                "defined_variable": "",

                "machine_code": [
                    {
                        "machine_code": "10101010",
                        "constant": "",
                    },
                    {
                        "machine_code": "",
                        "constant": "$other_variable",
                        "constant_type": "variable",
                    },
                ],
            },
        ],
        [
            {
                "line_no": 1,
                "raw": "@label1",
                "clean": "@label1",

                "defined_label": "@label1",
                "assigned_label": "",

                "defined_variable": "",

                "machine_code": [],
            },
            {
                "line_no": 2,
                "raw": "LOAD [$variable] A",
                "clean": "LOAD [$variable] A",

                "defined_label": "",
                "assigned_label": "@label1",

                "defined_variable": "",

                "machine_code": [
                    {
                        "machine_code": "10101010",
                        "constant": "",
                    },
                    {
                        "machine_code": "",
                        "constant": "$variable",
                        "constant_type": "variable",
                    },
                ],
            },
            {
                "line_no": 3,
                "raw": "@label2",
                "clean": "@label2",

                "defined_label": "@label2",
                "assigned_label": "",

                "defined_variable": "",

                "machine_code": [],
            },
            {
                "line_no": 4,
                "raw": "LOAD [$other_variable] A",
                "clean": "LOAD [$other_variable] A",

                "defined_label": "",
                "assigned_label": "@label2",

                "defined_variable": "",

                "machine_code": [
                    {
                        "machine_code": "10101010",
                        "constant": "",
                    },
                    {
                        "machine_code": "",
                        "constant": "$other_variable",
                        "constant_type": "variable",
                    },
                ],
            },
        ],
    ),
])
def test_assign_labels(test_input, expected):
    assembler.assign_labels(test_input)
    assert test_input == expected

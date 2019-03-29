import pytest
from copy import deepcopy

from eight_bit_computer.assembler import assembler
from eight_bit_computer.exceptions import LineProcessingError
from eight_bit_computer.language.utils import get_machine_code_byte_template


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


def get_assign_label_input_0():
    """
    A simple case with a label and a line under it.
    """
    input_line_1 = assembler.get_line_info_template()
    input_line_1["line_no"] = 1
    input_line_1["raw"] = "@label1"
    input_line_1["clean"] = "@label1"
    input_line_1["defined_label"] = "@label1"

    input_line_2 = assembler.get_line_info_template()
    input_line_2["line_no"] = 2
    input_line_2["raw"] = "LOAD [$variable] A"
    input_line_2["clean"] = "LOAD [$variable] A"
    input_line_2_mc_0 = get_machine_code_byte_template()
    input_line_2_mc_0["machine_code"] = "10101010"
    input_line_2_mc_1 = get_machine_code_byte_template()
    input_line_2_mc_1["constant"] = "$variable"
    input_line_2_mc_1["constant_type"] = "variable"
    input_line_2["machine_code"] = [input_line_2_mc_0, input_line_2_mc_1]

    expected_line_1 = deepcopy(input_line_1)

    expected_line_2 = deepcopy(input_line_2)
    expected_line_2["assigned_label"] = "@label1"

    return ([input_line_1, input_line_2], [expected_line_1, expected_line_2])


def get_assign_label_input_1():
    """
    A more complicated case with two labels and two lines.
    """
    input_line_1 = assembler.get_line_info_template()
    input_line_1["line_no"] = 1
    input_line_1["raw"] = "@label1"
    input_line_1["clean"] = "@label1"
    input_line_1["defined_label"] = "@label1"

    input_line_2 = assembler.get_line_info_template()
    input_line_2["line_no"] = 2
    input_line_2["raw"] = "LOAD [$variable] A"
    input_line_2["clean"] = "LOAD [$variable] A"
    input_line_2_mc_0 = get_machine_code_byte_template()
    input_line_2_mc_0["machine_code"] = "10101010"
    input_line_2_mc_1 = get_machine_code_byte_template()
    input_line_2_mc_1["constant"] = "$variable"
    input_line_2_mc_1["constant_type"] = "variable"
    input_line_2["machine_code"] = [input_line_2_mc_0, input_line_2_mc_1]

    input_line_3 = assembler.get_line_info_template()
    input_line_3["line_no"] = 3
    input_line_3["raw"] = "@label2"
    input_line_3["clean"] = "@label2"
    input_line_3["defined_label"] = "@label2"

    input_line_4 = assembler.get_line_info_template()
    input_line_4["line_no"] = 4
    input_line_4["raw"] = "LOAD [$other_variable] A"
    input_line_4["clean"] = "LOAD [$other_variable] A"
    input_line_4_mc_0 = get_machine_code_byte_template()
    input_line_4_mc_0["machine_code"] = "10101010"
    input_line_4_mc_1 = get_machine_code_byte_template()
    input_line_4_mc_1["constant"] = "$other_variable"
    input_line_4_mc_1["constant_type"] = "variable"
    input_line_4["machine_code"] = [input_line_2_mc_0, input_line_2_mc_1]

    expected_line_1 = deepcopy(input_line_1)

    expected_line_2 = deepcopy(input_line_2)
    expected_line_2["assigned_label"] = "@label1"

    expected_line_3 = deepcopy(input_line_3)

    expected_line_4 = deepcopy(input_line_4)
    expected_line_4["assigned_label"] = "@label2"

    return (
        [
            input_line_1,
            input_line_2,
            input_line_3,
            input_line_4,
        ],
        [
            expected_line_1,
            expected_line_2,
            expected_line_3,
            expected_line_4,
        ]
    )


@pytest.mark.parametrize("test_input,expected", [
    get_assign_label_input_0(),
    get_assign_label_input_1()
])
def test_assign_labels(test_input, expected):
    assembler.assign_labels(test_input)
    assert test_input == expected

import pytest
from copy import deepcopy

from eight_bit_computer.assembler import assembler
from eight_bit_computer.exceptions import LineProcessingError, AssemblyError
from eight_bit_computer.language.utils import get_machine_code_byte_template


@pytest.mark.parametrize("test_input,variable_start_offset", [
    (
        [
            "fegwkefjghwfjkhgwekjfgh",
        ],
        0,
    )
])
def test_lines_to_machine_code_raises(test_input, variable_start_offset):
    with pytest.raises(AssemblyError):
        assembler.lines_to_machine_code(
            test_input, variable_start_offset=variable_start_offset
        )


def get_process_line_test_data():
    """
    Test data for the process line test
    """
    tests = []
    test_input = ""
    test_output = assembler.get_line_info_template()
    tests.append((test_input, test_output))

    test_input = "// comment"
    test_output = assembler.get_line_info_template()
    test_output["raw"] = "// comment"
    tests.append((test_input, test_output))

    test_input = "@label"
    test_output = assembler.get_line_info_template()
    test_output["raw"] = "@label"
    test_output["clean"] = "@label"
    test_output["defined_label"] = "@label"
    tests.append((test_input, test_output))

    test_input = "$variable"
    test_output = assembler.get_line_info_template()
    test_output["raw"] = "$variable"
    test_output["clean"] = "$variable"
    test_output["defined_variable"] = "$variable"
    tests.append((test_input, test_output))

    test_input = "    @label // comment"
    test_output = assembler.get_line_info_template()
    test_output["raw"] = "    @label // comment"
    test_output["clean"] = "@label"
    test_output["defined_label"] = "@label"
    tests.append((test_input, test_output))

    test_input = "    $variable // comment"
    test_output = assembler.get_line_info_template()
    test_output["raw"] = "    $variable // comment"
    test_output["clean"] = "$variable"
    test_output["defined_variable"] = "$variable"
    tests.append((test_input, test_output))

    return tests


@pytest.mark.parametrize("test_input,expected", get_process_line_test_data())
def test_process_line(test_input, expected):
    assert assembler.process_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "fwgfkwghfkjhwgekjhgwkejg",
])
def test_process_line_raises(test_input):
    with pytest.raises(LineProcessingError):
        assembler.process_line(test_input)


@pytest.mark.parametrize("test_input,expected", [
    (
        "",
        "",
    ),
    (
        "//",
        "",
    ),
    (
        "/hello /world!",
        "/hello /world!",
    ),
    (
        "blah blah//",
        "blah blah",
    ),
    (
        "before//after",
        "before",
    ),
    (
        "   before   //after   ",
        "   before   ",
    ),
])
def test_remove_comments(test_input, expected):
    assert assembler.remove_comments(test_input) == expected


















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


def get_processed_assembly_lines():
    """
    The result of processing:

    ---
    $variable0
    @label1
        LOAD [$variable1] A

    @label2
        LOAD [$variable2] A
        JUMP @label1

        STORE A [#123]
    @label3
        LOAD [$variable3] B
        LOAD [$variable0] C
    $variable4
    ---
    """
    lines = []

    line = assembler.get_line_info_template()
    line["line_no"] = 1
    line["raw"] = "$variable0"
    line["clean"] = "$variable0"
    line["defined_variable"] = "$variable0"
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 2
    line["raw"] = "@label1"
    line["clean"] = "@label1"
    line["defined_label"] = "@label1"
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 3
    line["raw"] = "LOAD [$variable1] A"
    line["clean"] = "LOAD [$variable1] A"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["machine_code"] = "99999999"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["constant"] = "$variable1"
    line_mc_1["constant_type"] = "variable"
    line["machine_code"] = [line_mc_0, line_mc_1]
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 4
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 5
    line["raw"] = "@label2"
    line["clean"] = "@label2"
    line["defined_label"] = "@label2"
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 6
    line["raw"] = "LOAD [$variable2] A"
    line["clean"] = "LOAD [$variable2] A"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["machine_code"] = "99999999"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["constant"] = "$variable2"
    line_mc_1["constant_type"] = "variable"
    line["machine_code"] = [line_mc_0, line_mc_1]
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 7
    line["raw"] = "JUMP @label1"
    line["clean"] = "JUMP @label1"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["machine_code"] = "99999999"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["constant"] = "@label1"
    line_mc_1["constant_type"] = "label"
    line["machine_code"] = [line_mc_0, line_mc_1]
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 8
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 9
    line["raw"] = "STORE A [#123]"
    line["clean"] = "STORE A [#123]"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["machine_code"] = "99999999"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["constant"] = "#123"
    line_mc_1["constant_type"] = "number"
    line_mc_1["number_value"] = 123
    line["machine_code"] = [line_mc_0, line_mc_1]
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 10
    line["raw"] = "@label3"
    line["clean"] = "@label3"
    line["defined_label"] = "@label3"
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 11
    line["raw"] = "LOAD [$variable3] B"
    line["clean"] = "LOAD [$variable3] A"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["machine_code"] = "99999999"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["constant"] = "$variable3"
    line_mc_1["constant_type"] = "variable"
    line["machine_code"] = [line_mc_0, line_mc_1]
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 12
    line["raw"] = "LOAD [$variable0] C"
    line["clean"] = "LOAD [$variable0] A"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["machine_code"] = "99999999"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["constant"] = "$variable0"
    line_mc_1["constant_type"] = "variable"
    line["machine_code"] = [line_mc_0, line_mc_1]
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 13
    line["raw"] = "$variable4"
    line["clean"] = "$variable4"
    line["defined_variable"] = "$variable4"
    lines.append(line)

    return lines


def test_assign_labels():
    input_lines = get_processed_assembly_lines()
    expected_lines = deepcopy(input_lines)
    expected_lines[2]["assigned_label"] = "@label1"
    expected_lines[5]["assigned_label"] = "@label2"
    expected_lines[10]["assigned_label"] = "@label3"
    assembler.assign_labels(input_lines)
    assert input_lines == expected_lines


def test_resolve_labels():
    input_lines = get_processed_assembly_lines()
    input_lines[2]["assigned_label"] = "@label1"
    input_lines[5]["assigned_label"] = "@label2"
    input_lines[10]["assigned_label"] = "@label3"
    expected_lines = deepcopy(input_lines)
    expected_lines[6]["machine_code"][1]["machine_code"] = "00000000"
    assembler.resolve_labels(input_lines)
    assert input_lines == expected_lines


def test_label_map():
    input_lines = get_processed_assembly_lines()
    input_lines[2]["assigned_label"] = "@label1"
    input_lines[5]["assigned_label"] = "@label2"
    input_lines[10]["assigned_label"] = "@label3"
    expected_label_map = {
        "@label1": "00000000",
        "@label2": "00000010",
        "@label3": "00001000",
    }
    label_map = assembler.create_label_map(input_lines)
    assert label_map == expected_label_map


def test_resolve_numbers():
    input_lines = get_processed_assembly_lines()
    expected_lines = deepcopy(input_lines)
    expected_lines[8]["machine_code"][1]["machine_code"] = "01111011"
    assembler.resolve_numbers(input_lines)
    assert input_lines == expected_lines


def test_resolve_variables_no_offset():
    input_lines = get_processed_assembly_lines()
    expected_lines = deepcopy(input_lines)
    expected_lines[2]["machine_code"][1]["machine_code"] = "00000001"
    expected_lines[5]["machine_code"][1]["machine_code"] = "00000010"
    expected_lines[10]["machine_code"][1]["machine_code"] = "00000011"
    expected_lines[11]["machine_code"][1]["machine_code"] = "00000000"
    assembler.resolve_variables(input_lines)
    assert input_lines == expected_lines


def test_resolve_variables_with_offset():
    input_lines = get_processed_assembly_lines()
    expected_lines = deepcopy(input_lines)
    expected_lines[2]["machine_code"][1]["machine_code"] = "00001001"
    expected_lines[5]["machine_code"][1]["machine_code"] = "00001010"
    expected_lines[10]["machine_code"][1]["machine_code"] = "00001011"
    expected_lines[11]["machine_code"][1]["machine_code"] = "00001000"
    assembler.resolve_variables(input_lines, variable_start_offset=8)
    assert input_lines == expected_lines


def test_create_variable_map_no_offset():
    input_lines = get_processed_assembly_lines()
    exected_variable_map = {
        "$variable0": "00000000",
        "$variable1": "00000001",
        "$variable2": "00000010",
        "$variable3": "00000011",
        "$variable4": "00000100",
    }
    variable_map = assembler.create_variable_map(input_lines)
    assert variable_map == exected_variable_map


def test_create_variable_map_with_offset():
    input_lines = get_processed_assembly_lines()
    exected_variable_map = {
        "$variable0": "00001000",
        "$variable1": "00001001",
        "$variable2": "00001010",
        "$variable3": "00001011",
        "$variable4": "00001100",
    }
    variable_map = assembler.create_variable_map(
        input_lines, variable_start_offset=8
    )
    assert variable_map == exected_variable_map

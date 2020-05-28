import pytest
from copy import deepcopy

from eight_bit_computer import main
from eight_bit_computer.data_structures import (
    get_assembly_line_template, get_machine_code_byte_template
)

@pytest.mark.parametrize("test_input,expected", [
    (
        "a.asm",
        "a.mc",
    ),
    (
        "foo.asm",
        "foo.mc",
    ),
])
def test_get_mc_filepath(test_input, expected):
    assert main.get_mc_filepath(test_input) == expected


def gen_test_extract_variables_data():
    ret = []

    lines = []
    line1 = get_assembly_line_template()
    line1["defines_variable"] = True
    line1["defined_variable"] = "$var1"
    line1["defined_variable_location"] = 0
    line1["defined_variable_value"] = 1
    lines.append(line1)

    res = ["00000001"]

    ret.append((lines, res))


    lines = []
    line1 = get_assembly_line_template()
    line1["defines_variable"] = True
    line1["defined_variable"] = "$var1"
    line1["defined_variable_location"] = 0
    line1["defined_variable_value"] = 1
    lines.append(line1)

    line2 = get_assembly_line_template()
    line2["defines_variable"] = True
    line2["defined_variable"] = "$var2"
    line2["defined_variable_location"] = 1
    line2["defined_variable_value"] = 5
    lines.append(line2)

    res = ["00000001", "00000101"]

    ret.append((lines, res))

    lines = []
    line1 = get_assembly_line_template()
    line1["defines_variable"] = True
    line1["defined_variable"] = "$var1"
    line1["defined_variable_location"] = 2
    line1["defined_variable_value"] = 255
    lines.append(line1)

    res = ["00000000", "00000000", "11111111"]

    ret.append((lines, res))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", gen_test_extract_variables_data()
)
def test_extract_variables(test_input, expected):
    assert main.extract_variables(test_input) == expected


def gen_test_combine_mc_and_variable_bitstrings_data():
    ret = []

    mc_bitstrings = []
    variable_bitstrings = []
    res = []
    ret.append((mc_bitstrings, variable_bitstrings, res))

    mc_bitstrings = ["00001000"]
    variable_bitstrings = []
    res = ["00001000"]
    ret.append((mc_bitstrings, variable_bitstrings, res))

    mc_bitstrings = ["00001000", "00001001"]
    variable_bitstrings = []
    res = ["00001000", "00001001"]
    ret.append((mc_bitstrings, variable_bitstrings, res))

    mc_bitstrings = ["00001000", "00001001"]
    variable_bitstrings = ["00001111"]
    res = (["00001000", "00001001"] + ["00000000"] * 254) + ["00001111"]
    ret.append((mc_bitstrings, variable_bitstrings, res))

    return ret


@pytest.mark.parametrize(
    "mc_bitstrings,variable_bitstrings,expected",
    gen_test_combine_mc_and_variable_bitstrings_data()
)
def test_combine_mc_and_variable_bitstrings(mc_bitstrings, variable_bitstrings, expected):
    assert main.combine_mc_and_variable_bitstrings(mc_bitstrings, variable_bitstrings) == expected
import pytest

from sixteen_bit_computer.operations import jump_if_gt_acc_op
from sixteen_bit_computer.data_structures import get_machine_code_byte_template
from sixteen_bit_computer.exceptions import OperationParsingError


def generate_parse_line_test_data():
    ret = []

    test_input = ""
    expected = []
    ret.append((test_input, expected))

    test_input = "   \t"
    expected = []
    ret.append((test_input, expected))

    test_input = "LOAD [#123] A"
    expected = []
    ret.append((test_input, expected))

    test_input = "JUMP_IF_GT_ACC A @label"
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "10110001"

    mc_1 = get_machine_code_byte_template()
    mc_1["byte_type"] = "constant"
    mc_1["constant"] = "@label"
    ret.append((test_input, [mc_0, mc_1]))

    test_input = "   JUMP_IF_GT_ACC B #123   "
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "10110010"

    mc_1 = get_machine_code_byte_template()
    mc_1["byte_type"] = "constant"
    mc_1["constant"] = "#123"
    ret.append((test_input, [mc_0, mc_1]))

    test_input = "   JUMP_IF_GT_ACC #55 #123   "
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "10110111"

    mc_1 = get_machine_code_byte_template()
    mc_1["byte_type"] = "constant"
    mc_1["constant"] = "#55"

    mc_2 = get_machine_code_byte_template()
    mc_2["byte_type"] = "constant"
    mc_2["constant"] = "#123"
    ret.append((test_input, [mc_0, mc_1, mc_2]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert jump_if_gt_acc_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "JUMP_IF_GT_ACC",
    "JUMP_IF_GT_ACC A",
    "JUMP_IF_GT_ACC A B",
    "JUMP_IF_GT_ACC #123 A",
    "JUMP_IF_GT_ACC BLAH",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        jump_if_gt_acc_op.parse_line(test_input)

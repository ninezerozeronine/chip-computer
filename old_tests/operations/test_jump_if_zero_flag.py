import pytest

from eight_bit_computer.operations import jump_if_zero_flag
from eight_bit_computer.data_structures import get_machine_code_byte_template
from eight_bit_computer.exceptions import OperationParsingError


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

    test_input = "JUMP_IF_ZERO_FLAG @label"
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "00000000"
    mc_1 = get_machine_code_byte_template()
    mc_1["byte_type"] = "constant"
    mc_1["constant"] = "@label"
    ret.append((test_input, [mc_0, mc_1]))

    test_input = "   JUMP_IF_ZERO_FLAG #123   "
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "00000000"
    mc_1 = get_machine_code_byte_template()
    mc_1["byte_type"] = "constant"
    mc_1["constant"] = "#123"
    ret.append((test_input, [mc_0, mc_1]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert jump_if_zero_flag.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "JUMP_IF_ZERO_FLAG",
    "JUMP_IF_ZERO_FLAG A",
    "JUMP_IF_ZERO_FLAG A B",
    "JUMP_IF_ZERO_FLAG #123 @label",
    "JUMP_IF_ZERO_FLAG BLAH",
    "JUMP_IF_ZERO_FLAG @l1 @l2",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        jump_if_zero_flag.parse_line(test_input)

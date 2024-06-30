import pytest

from sixteen_bit_computer.operations import jump_if_eq_zero_op
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

    test_input = "JUMP_IF_EQ_ZERO A @label"
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "10100001"

    mc_1 = get_machine_code_byte_template()
    mc_1["byte_type"] = "constant"
    mc_1["constant"] = "@label"
    ret.append((test_input, [mc_0, mc_1]))

    test_input = "   JUMP_IF_EQ_ZERO B #123   "
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "10100010"

    mc_1 = get_machine_code_byte_template()
    mc_1["byte_type"] = "constant"
    mc_1["constant"] = "#123"
    ret.append((test_input, [mc_0, mc_1]))

    test_input = "JUMP_IF_EQ_ZERO PC #55"
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "10100101"

    mc_1 = get_machine_code_byte_template()
    mc_1["byte_type"] = "constant"
    mc_1["constant"] = "#55"

    ret.append((test_input, [mc_0, mc_1]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert jump_if_eq_zero_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "JUMP_IF_EQ_ZERO",
    "JUMP_IF_EQ_ZERO A",
    "JUMP_IF_EQ_ZERO A B",
    "JUMP_IF_EQ_ZERO #123 A",
    "JUMP_IF_EQ_ZERO BLAH",
    "JUMP_IF_EQ_ZERO #123",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        jump_if_eq_zero_op.parse_line(test_input)

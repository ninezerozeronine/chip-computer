import pytest

from sixteen_bit_computer.operations import jump
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

    test_input = "JUMP A"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "00001101"
    ret.append((test_input, [mc]))

    test_input = "JUMP ACC"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "00000101"
    ret.append((test_input, [mc]))

    test_input = "JUMP [C]"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "01011101"
    ret.append((test_input, [mc]))

    test_input = "JUMP @label"
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "00111101"

    mc_1 = get_machine_code_byte_template()
    mc_1["byte_type"] = "constant"
    mc_1["constant"] = "@label"
    ret.append((test_input, [mc_0, mc_1]))

    test_input = "JUMP [$var]"
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "01111101"

    mc_1 = get_machine_code_byte_template()
    mc_1["byte_type"] = "constant"
    mc_1["constant"] = "$var"
    ret.append((test_input, [mc_0, mc_1]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert jump.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "JUMP",
    "JUMP PC",
    "JUMP CONST",
    "JUMP #123 A",
    "JUMP A A",
    "JUMP B B",
    "JUMP SP SP",
    "JUMP A B C",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        jump.parse_line(test_input)

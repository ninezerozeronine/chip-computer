import pytest

from sixteen_bit_computer.operations import nor_op
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

    test_input = "NOR C"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11101011"
    ret.append((test_input, [mc]))

    test_input = "NOR B"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11101010"
    ret.append((test_input, [mc]))

    test_input = "   NOR  #123   "
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "11101000"

    mc_1 = get_machine_code_byte_template()
    mc_1["byte_type"] = "constant"
    mc_1["constant"] = "#123"
    ret.append((test_input, [mc_0, mc_1]))

    test_input = "NOR #0b00101111"
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "11101000"

    mc_1 = get_machine_code_byte_template()
    mc_1["byte_type"] = "constant"
    mc_1["constant"] = "#0b00101111"
    ret.append((test_input, [mc_0, mc_1]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert nor_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "NOR",
    "NOR PC",
    "NOR A B",
    "NOR ACCS",
    "NOR BLAH #123",
    "NOR A #123 FOO",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        nor_op.parse_line(test_input)

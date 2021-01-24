import pytest

from eight_bit_computer.operations import set_zero_op
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

    test_input = "  SET_ZERO ACC"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11000000"
    ret.append((test_input, [mc]))

    test_input = "SET_ZERO B  "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11000010"
    ret.append((test_input, [mc]))

    test_input = "   SET_ZERO  C   "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11000011"
    ret.append((test_input, [mc]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert set_zero_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "SET_ZERO",
    "SET_ZERO   ",
    "SET_ZERO PC",
    "SET_ZERO A B",
    "SET_ZERO ACCS",
    "SET_ZERO BLAH #123",
    "SET_ZERO A #123 FOO",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        set_zero_op.parse_line(test_input)

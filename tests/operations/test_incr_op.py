import pytest

from eight_bit_computer.operations import incr_op
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

    test_input = "  INCR ACC"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11000100"
    ret.append((test_input, [mc]))

    test_input = "INCR B  "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11000110"
    ret.append((test_input, [mc]))

    test_input = "   INCR  C   "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11000111"
    ret.append((test_input, [mc]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert incr_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "INCR",
    "INCR   ",
    "INCR PC",
    "INCR A B",
    "INCR ACCS",
    "INCR BLAH #123",
    "INCR A #123 FOO",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        incr_op.parse_line(test_input)

import pytest

from eight_bit_computer.operations import call_op
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

    test_input = "  CALL ACC"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "01000110"
    ret.append((test_input, [mc]))

    test_input = "CALL B  "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "01010110"
    ret.append((test_input, [mc]))

    test_input = "   CALL  C   "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "01011110"
    ret.append((test_input, [mc]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert call_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "CALL",
    "CALL   ",
    "CALL #123",
    "CALL SP",
    "CALL A B",
    "CALL ACCS",
    "CALL BLAH #123",
    "CALL A #123 FOO",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        call_op.parse_line(test_input)

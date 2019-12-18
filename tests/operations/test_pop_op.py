import pytest

from eight_bit_computer.operations import pop_op
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

    test_input = "  POP ACC"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "01110000"
    ret.append((test_input, [mc]))

    test_input = "POP B  "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "01110010"
    ret.append((test_input, [mc]))

    test_input = "   POP  C   "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "01110011"
    ret.append((test_input, [mc]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert pop_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "POP",
    "POP   ",
    "POP #123",
    "POP SP",
    "POP A B",
    "POP ACCS",
    "POP BLAH #123",
    "POP A #123 FOO",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        pop_op.parse_line(test_input)

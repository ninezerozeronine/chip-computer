import pytest

from sixteen_bit_computer.operations import not_op
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

    test_input = "  NOT ACC"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11110100"
    ret.append((test_input, [mc]))

    test_input = "NOT B  "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11110110"
    ret.append((test_input, [mc]))

    test_input = "   NOT  C   "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11110111"
    ret.append((test_input, [mc]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert not_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "NOT",
    "NOT PC",
    "NOT A B",
    "NOT ACCS",
    "NOT BLAH #123",
    "NOT A #123 FOO",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        not_op.parse_line(test_input)

import pytest

from sixteen_bit_computer.operations import decr_op
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

    test_input = "  DECR ACC"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11001000"
    ret.append((test_input, [mc]))

    test_input = "DECR B  "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11001010"
    ret.append((test_input, [mc]))

    test_input = "   DECR  C   "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11001011"
    ret.append((test_input, [mc]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert decr_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "DECR",
    "DECR   ",
    "DECR PC",
    "DECR A B",
    "DECR ACCS",
    "DECR BLAH #123",
    "DECR A #123 FOO",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        decr_op.parse_line(test_input)

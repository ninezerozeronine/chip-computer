import pytest

from sixteen_bit_computer.operations import lshiftc_op
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

    test_input = "  LSHIFTC ACC"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11111100"
    ret.append((test_input, [mc]))

    test_input = "LSHIFTC B  "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11111110"
    ret.append((test_input, [mc]))

    test_input = "   LSHIFTC  C   "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "11111111"
    ret.append((test_input, [mc]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert lshiftc_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "LSHIFTC",
    "LSHIFTC PC",
    "LSHIFTC A B",
    "LSHIFTC ACCS",
    "LSHIFTC BLAH #123",
    "LSHIFTC A #123 FOO",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        lshiftc_op.parse_line(test_input)

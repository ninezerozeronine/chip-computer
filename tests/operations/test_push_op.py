import pytest

from eight_bit_computer.operations import push_op
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

    test_input = "  PUSH ACC"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "10000110"
    ret.append((test_input, [mc]))

    test_input = "PUSH B  "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "10010110"
    ret.append((test_input, [mc]))

    test_input = "   PUSH  PC   "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "10101110"
    ret.append((test_input, [mc]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert push_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "PUSH",
    "PUSH   ",
    "PUSH #123",
    "PUSH SP",
    "PUSH A B",
    "PUSH ACCS",
    "PUSH BLAH #123",
    "PUSH A #123 FOO",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        push_op.parse_line(test_input)

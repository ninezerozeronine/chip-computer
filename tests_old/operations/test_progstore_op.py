import pytest

from sixteen_bit_computer.operations import progstore_op
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

    test_input = "COPY [#123] A"
    expected = []
    ret.append((test_input, expected))

    test_input = "PROGSTORE [B]"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "10111010"
    ret.append((test_input, [mc]))

    test_input = "   PROGSTORE   [$variable]   "
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "10111111"
    mc_1 = get_machine_code_byte_template()
    mc_1["byte_type"] = "constant"
    mc_1["constant"] = "$variable"
    ret.append((test_input, [mc_0, mc_1]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert progstore_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "PROGSTORE",
    "PROGSTORE A",
    "PROGSTORE #123",
    "PROGSTORE IMM",
    "PROGSTORE #123 A",
    "PROGSTORE A A",
    "PROGSTORE [B] A",
    "PROGSTORE [$foo] SP"
    "PROGSTORE SP [B]",
    "PROGSTORE A B C",
    "PROGSTORE []",
    "PROGSTORE [] A",
    "PROGSTORE [$var] FOO",
    "PROGSTORE [notvalid] FOO",
    "PROGSTORE [#123] A",
    "PROGSTORE [A] B C",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        progstore_op.parse_line(test_input)

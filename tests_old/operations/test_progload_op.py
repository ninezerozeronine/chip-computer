import pytest

from sixteen_bit_computer.operations import progload_op
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

    test_input = "PROGLOAD [C]"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "01011111"
    ret.append((test_input, [mc]))

    test_input = "   PROGLOAD  [$variable]    "
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "01111111"
    mc_1 = get_machine_code_byte_template()
    mc_1["byte_type"] = "constant"
    mc_1["constant"] = "$variable"
    ret.append((test_input, [mc_0, mc_1]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert progload_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "PROGLOAD",
    "PROGLOAD A",
    "PROGLOAD #123",
    "PROGLOAD $var",
    "PROGLOAD IMM",
    "PROGLOAD #123 A",
    "PROGLOAD B B",
    "PROGLOAD A B C",
    "PROGLOAD []",
    "PROGLOAD [] A",
    "PROGLOAD [$var] FOO",
    "PROGLOAD [notvalid] FOO",
    "PROGLOAD [#123] A",
    "PROGLOAD [A] B C",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        progload_op.parse_line(test_input)

import pytest

from sixteen_bit_computer.operations import store_op
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

    test_input = "STORE C [A]"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "10011001"
    ret.append((test_input, [mc]))

    test_input = "   STORE  ACC [$variable]   "
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "10000111"
    mc_1 = get_machine_code_byte_template()
    mc_1["byte_type"] = "constant"
    mc_1["constant"] = "$variable"
    ret.append((test_input, [mc_0, mc_1]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert store_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "STORE",
    "STORE A",
    "STORE #123",
    "STORE IMM",
    "STORE #123 A",
    "STORE A A",
    "STORE [B] A",
    "STORE [$foo] SP"
    "STORE SP [B]",
    "STORE A B C",
    "STORE []",
    "STORE [A]",
    "STORE [] A",
    "STORE [$var] FOO",
    "STORE [notvalid] FOO",
    "STORE [#123] A",
    "STORE [A] B C",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        store_op.parse_line(test_input)

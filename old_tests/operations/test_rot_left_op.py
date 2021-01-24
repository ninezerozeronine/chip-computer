import pytest

from eight_bit_computer.operations import rot_left_op
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

    test_input = "ROT_LEFT A"
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "10100111"
    ret.append((test_input, [mc_0]))

    test_input = "   ROT_LEFT B   "
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "10110000"
    ret.append((test_input, [mc_0]))

    test_input = "ROT_LEFT ACC"
    mc_0 = get_machine_code_byte_template()
    mc_0["byte_type"] = "instruction"
    mc_0["bitstring"] = "10100110"
    ret.append((test_input, [mc_0]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert rot_left_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "ROT_LEFT",
    "ROT_LEFT A B",
    "ROT_LEFT #123 A",
    "ROT_LEFT BLAH",
    "ROT_LEFT #123",
])
def test_parse_line_raises(test_input):
    with pytest.raises(OperationParsingError):
        rot_left_op.parse_line(test_input)

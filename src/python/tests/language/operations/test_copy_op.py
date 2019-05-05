import pytest

from eight_bit_computer.language.operations import copy_op
from eight_bit_computer.language.utils import get_machine_code_byte_template
from eight_bit_computer.exceptions import InstructionParsingError


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

    test_input = "COPY A B"
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "00001010"
    ret.append((test_input, [mc]))

    test_input = "   COPY  B   A   "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["bitstring"] = "00010001"
    ret.append((test_input, [mc]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert copy_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_input", [
    "COPY",
    "COPY A",
    "COPY #123",
    "COPY IMM",
    "COPY #123 A",
    "COPY A A",
    "COPY B B",
    "COPY SP SP",
    "COPY A B C",
])
def test_parse_line_raises(test_input):
    with pytest.raises(InstructionParsingError):
        copy_op.parse_line(test_input)

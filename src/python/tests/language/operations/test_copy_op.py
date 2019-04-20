import pytest

from eight_bit_computer.language.operations import copy_op
from eight_bit_computer.language.utils import get_machine_code_byte_template
from eight_bit_computer.exceptions import InstructionParsingError


@pytest.mark.parametrize("test_source,test_dest,expected", [
    (
        "A",
        "B",
        "00001010",
    ),
    (
        "B",
        "A",
        "00010001",
    ),
])
def test_get_instruction_byte(test_source, test_dest, expected):
    assert copy_op.get_instruction_byte(test_source, test_dest) == expected


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
    mc["machine_code"] = "00001010"
    ret.append((test_input, [mc]))

    test_input = "   COPY  B   A   "
    mc = get_machine_code_byte_template()
    mc["byte_type"] = "instruction"
    mc["machine_code"] = "00010001"
    ret.append((test_input, [mc]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert copy_op.parse_line(test_input) == expected


@pytest.mark.parametrize("test_src,test_dest", [
    ("A", "A"),
    ("SP", "SP"),
    ("FOO", "A"),
    ("C", "BAR"),
])
def test_validate_source_and_dest_raises(test_src, test_dest):
    with pytest.raises(InstructionParsingError):
        copy_op.validate_source_and_dest(test_src, test_dest)


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

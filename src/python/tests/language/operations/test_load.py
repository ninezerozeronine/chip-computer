import pytest

from eight_bit_computer.language.operations import load
from eight_bit_computer.language.utils import get_machine_code_byte_template
from eight_bit_computer.exceptions import InstructionParsingError


@pytest.mark.parametrize("test_source,test_dest,expected", [
    (
        "A",
        "B",
        "01001010",
    ),
    (
        "IMM",
        "C",
        "01111011",
    ),
])
def test_get_instruction_byte(test_source, test_dest, expected):
    assert load.get_instruction_byte(test_source, test_dest) == expected


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

    test_input = "LOAD [C] A"
    mc = get_machine_code_byte_template()
    mc["machine_code"] = "01011001"
    ret.append((test_input, [mc]))

    test_input = "   LOAD  [$variable]   ACC   "
    mc_0 = get_machine_code_byte_template()
    mc_0["machine_code"] = "01111000"
    mc_1 = get_machine_code_byte_template()
    mc_1["constant"] = "$variable"
    ret.append((test_input, [mc_0, mc_1]))

    return ret


@pytest.mark.parametrize(
    "test_input,expected", generate_parse_line_test_data()
)
def test_parse_line(test_input, expected):
    assert load.parse_line(test_input) == expected


@pytest.mark.parametrize("test_src,test_dest", [
    ("A", "B"),
    ("FOO", "A"),
    ("C", "BAR"),
    ("[]", "BAR"),
    ("[#123]", "[C]"),
    ("[C]", "BAR"),
])
def test_validate_source_and_dest_raises(test_src, test_dest):
    with pytest.raises(InstructionParsingError):
        load.validate_source_and_dest_tokens(test_src, test_dest)


@pytest.mark.parametrize("test_input", [
    "LOAD",
    "LOAD A",
    "LOAD #123",
    "LOAD IMM",
    "LOAD #123 A",
    "LOAD A A",
    "LOAD B B",
    "LOAD SP SP",
    "LOAD A B C",
    "LOAD []",
    "LOAD [A]",
    "LOAD [] A",
    "LOAD [$var] FOO",
    "LOAD [#123 A",
    "LOAD [A] B C",
])
def test_parse_line_raises(test_input):
    with pytest.raises(InstructionParsingError):
        load.parse_line(test_input)

import pytest
from copy import deepcopy

from eight_bit_computer import main
from eight_bit_computer.data_structures import (
    get_assembly_line_template, get_machine_code_byte_template
)

@pytest.mark.parametrize("test_input,expected", [
    (
        "a.asm",
        "a.mc",
    ),
    (
        "foo.asm",
        "foo.mc",
    ),
])
def test_get_mc_filename(test_input, expected):
    assert main.get_mc_filename(test_input) == expected

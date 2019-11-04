"""
XOR Operation
"""

from . import simple_alu_op_base

from ..language_defs import (
    ALU_OPERATIONS,
    ALU_CONTROL_FLAGS,
    instruction_byte_from_bitdefs,
)

_NAME = "XOR"


def generate_microcode_templates():
    """
    Generate microcode for all the XOR instructions.

    Returns:
        list(DataTemplate): DataTemplates for all the XOR instructions.
    """

    return simple_alu_op_base.generate_microcode_templates(
        ALU_OPERATIONS["XOR"],
        ALU_CONTROL_FLAGS["A_XOR_B"],
    )


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a XOR assembly line, return an empty
    list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of machine code byte template dictionaries or
        an empty list.
    """

    return simple_alu_op_base.parse_line(
        line, _NAME, ALU_OPERATIONS["XOR"]
    )

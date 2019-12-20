"""
The JUMP_IF_GTE_ACC operation.

Sets PC (jumps) to a constant if the module passed as an argument is
greater than or equal to the value in ACC.

This operation will generate and store (clobber) ALU flags.
"""

from ..language_defs import (
    INSTRUCTION_GROUPS,
    DEST_REGISTERS,
    SRC_REGISTERS,
    ALU_CONTROL_FLAGS,
    FLAGS,
)

from . import jump_if_comparison_base
from ..operation_utils import assemble_instruction, match_and_parse_line
from ..data_structures import (
    get_arg_def_template, get_machine_code_byte_template
)

_NAME = "JUMP_IF_GTE_ACC"


def generate_microcode_templates():
    """
    Generate microcode for all the JUMP_IF_GTE_ACC operations.

    Returns:
        list(DataTemplate): DataTemplates for all the JUMP_IF_GTE_ACC
        microcode.
    """

    return jump_if_comparison_base.generate_microcode_templates(
        INSTRUCTION_GROUPS["LOAD"],
        DEST_REGISTERS["SP"],
        SRC_REGISTERS,
        ALU_CONTROL_FLAGS["COMPARE_LT_GTE"],
        [FLAGS["CARRY_BORROW"]["LOW"]],
        [FLAGS["CARRY_BORROW"]["HIGH"]],
    )


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably an JUMP_IF_GTE_ACC assembly line,
    return an empty list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of instruction byte template dictionaries or an
        empty list.
    """

    return jump_if_comparison_base.parse_line(
        line,
        _NAME,
        INSTRUCTION_GROUPS["LOAD"],
        DEST_REGISTERS["SP"],
        SRC_REGISTERS,
    )

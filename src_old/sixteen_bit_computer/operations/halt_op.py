"""
The HALT operation.

Halts execution of the computer by stopping the clock.
"""

from itertools import product

from ..language_defs import (
    INSTRUCTION_GROUPS,
    SRC_REGISTERS,
    DEST_REGISTERS,
    MODULE_CONTROL,
    FLAGS,
    instruction_byte_from_bitdefs,
)

from ..operation_utils import assemble_instruction, match_and_parse_line
from ..data_structures import get_machine_code_byte_template

_NAME = "HALT"


def generate_microcode_templates():
    """
    Generate microcode for the HALT operation.

    Returns:
        list(DataTemplate): DataTemplates for all the HALT microcode.
    """
    instruction_byte_bitdefs = generate_instruction_byte_bitdefs()
    flags_bitdefs = [FLAGS["ANY"]]
    control_steps = [
        [MODULE_CONTROL["CLOCK"]["HALT"]]
    ]

    return assemble_instruction(
        instruction_byte_bitdefs, flags_bitdefs, control_steps
    )


def generate_instruction_byte_bitdefs():
    """
    Generate bitdefs to specify the HALT instruction.

    Returns:
        list(str): Bitdefs that make up the instruction_byte
    """

    return [
        INSTRUCTION_GROUPS["STORE"],
        SRC_REGISTERS["SP+/-"],
        DEST_REGISTERS["SP+/-"],
    ]


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably an HALT assembly line, return an
    empty list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of instruction byte template dictionaries or an
        empty list.
    """

    match, signature = match_and_parse_line(line, _NAME)

    if not match:
        return []

    instruction_byte = instruction_byte_from_bitdefs(
        generate_instruction_byte_bitdefs()
    )
    mc_byte = get_machine_code_byte_template()
    mc_byte["byte_type"] = "instruction"
    mc_byte["bitstring"] = instruction_byte

    return [mc_byte]

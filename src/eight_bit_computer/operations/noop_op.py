"""
The NOOP operation.

Does nothing for one micro cycle.
"""

from itertools import product

from ..language_defs import (
    INSTRUCTION_GROUPS,
    SRC_REGISTERS,
    DEST_REGISTERS,
    MODULE_CONTROLS_NONE,
    FLAGS,
    instruction_byte_from_bitdefs,
)

from ..operation_utils import assemble_instruction, match_and_parse_line
from ..data_structures import get_machine_code_byte_template

_NAME = "NOOP"


def generate_microcode_templates():
    """
    Generate microcode for the NOOP operation.

    Returns:
        list(DataTemplate): DataTemplates for all the NOOP microcode.
    """
    instruction_byte_bitdefs = generate_instruction_byte_bitdefs()
    flags_bitdefs = [FLAGS["ANY"]]
    control_steps = [[MODULE_CONTROLS_NONE]]

    return assemble_instruction(
        instruction_byte_bitdefs, flags_bitdefs, control_steps
    )


def generate_instruction_byte_bitdefs():
    """
    Generate bitdefs to specify the NOOP instruction.

    Returns:
        list(str): Bitdefs that make up the instruction_byte
    """

    return [
        INSTRUCTION_GROUPS["LOAD"],
        SRC_REGISTERS["SP+/-"],
        DEST_REGISTERS["SP+/-"],
    ]


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably an NOOP assembly line, return an
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

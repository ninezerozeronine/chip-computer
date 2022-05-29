"""
The RETURN operation.

Pops the top of the stack into the program counter.

Expects to be used after having arrived at a section of assembly with the
CALL instruction.
"""

from itertools import product

from ..language_defs import (
    INSTRUCTION_GROUPS,
    SRC_REGISTERS,
    DEST_REGISTERS,
    MODULE_CONTROL,
    FLAGS,
    ALU_CONTROL_FLAGS,
    instruction_byte_from_bitdefs,
)

from ..operation_utils import assemble_instruction, match_and_parse_line
from ..data_structures import get_machine_code_byte_template

_NAME = "RETURN"


def generate_microcode_templates():
    """
    Generate microcode for the RETURN operation.

    Returns:
        list(DataTemplate): DataTemplates for all the RETURN microcode.
    """
    instruction_byte_bitdefs = generate_instruction_byte_bitdefs()
    flags_bitdefs = [FLAGS["ANY"]]

    sp_into_mar = [
        MODULE_CONTROL["SP"]["OUT"],
        MODULE_CONTROL["MAR"]["IN"],
    ]

    ram_into_pc = [
        MODULE_CONTROL["RAM"]["OUT"],
        MODULE_CONTROL["PC"]["IN"],
    ]

    incr_sp = [
        MODULE_CONTROL["SP"]["OUT"],
        MODULE_CONTROL["ALU"]["A_IS_BUS"],
        MODULE_CONTROL["ALU"]["STORE_RESULT"],
    ]
    incr_sp.extend(ALU_CONTROL_FLAGS["A_PLUS_1"])

    alu_into_sp = [
        MODULE_CONTROL["ALU"]["OUT"],
        MODULE_CONTROL["SP"]["IN"],
    ]

    control_steps = [
        sp_into_mar,
        ram_into_pc,
        incr_sp,
        alu_into_sp,
    ]

    return assemble_instruction(
        instruction_byte_bitdefs, flags_bitdefs, control_steps
    )


def generate_instruction_byte_bitdefs():
    """
    Generate bitdefs to specify the RETURN instruction.

    Returns:
        list(str): Bitdefs that make up the instruction_byte
    """

    return [
        INSTRUCTION_GROUPS["LOAD"],
        SRC_REGISTERS["SP+/-"],
        DEST_REGISTERS["PC"],
    ]


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably an RETURN assembly line, return an
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

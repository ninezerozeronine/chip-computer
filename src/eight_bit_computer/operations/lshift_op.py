"""
The LSHIFT operation.

Moves all the bits in the argument one place to the left (toward the
most significant bit) in place. A zero is added in the
rightmost (least significant bit) place.
"""

from itertools import product

from ..language_defs import (
    INSTRUCTION_GROUPS,
    MODULE_CONTROL,
    ALU_CONTROL_FLAGS,
    ALU_OPERATIONS,
    ALU_OPERANDS,
    FLAGS,
    instruction_byte_from_bitdefs,
)

from ..operation_utils import assemble_instruction, match_and_parse_line
from ..data_structures import (
    get_arg_def_template, get_machine_code_byte_template
)

_NAME = "LSHIFT"


def generate_signatures():
    """
    Generate the definitions of all possible arguments passable.

    Returns:
        list(list(dict)): All possible arguments. See
        :func:`~.get_arg_def_template` for more information.
    """

    signatures = []
    for register in ("ACC", "A", "B", "C"):
        signature = []

        arg_def = get_arg_def_template()
        arg_def["value_type"] = "module_name"
        arg_def["value"] = register
        signature.append(arg_def)

        signatures.append(signature)

    return signatures


def generate_microcode_templates():
    """
    Generate microcode for all the LSHIFT operations.

    Returns:
        list(DataTemplate): DataTemplates for all the LSHIFT microcode.
    """

    data_templates = []

    signatures = generate_signatures()
    for signature in signatures:
        templates = generate_operation_templates(signature)
        data_templates.extend(templates)

    return data_templates


def generate_operation_templates(signature):
    """
    Create the DataTemplates to define an LSHIFT with the given args.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular not operation to generate
            templates for.
    Returns:
        list(DataTemplate) : Datatemplates that define this not.
    """
    instruction_byte_bitdefs = generate_instruction_byte_bitdefs(signature)

    flags_bitdefs = [FLAGS["ANY"]]

    step_0 = [
        MODULE_CONTROL[signature[0]["value"]]["OUT"],
        MODULE_CONTROL["ALU"]["A_IS_BUS"],
        MODULE_CONTROL["ALU"]["STORE_RESULT"],
        MODULE_CONTROL["ALU"]["STORE_FLAGS"],
    ]
    step_0.extend(ALU_CONTROL_FLAGS["A_PLUS_A"])

    step_1 = [
        MODULE_CONTROL["ALU"]["OUT"],
        MODULE_CONTROL[signature[0]["value"]]["IN"],
    ]

    control_steps = [step_0, step_1]

    return assemble_instruction(
        instruction_byte_bitdefs, flags_bitdefs, control_steps
    )


def generate_instruction_byte_bitdefs(signature):
    """
    Generate bitdefs to specify the instruction byte for these args.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular not operation to generate
            the instruction byte bitdefs for.
    Returns:
        list(str): Bitdefs that make up the instruction_byte
    """

    if signature[0]["value"] == "ACC":
        alu_operands = ALU_OPERANDS["ACC/CONST"]
    else:
        alu_operands = ALU_OPERANDS[signature[0]["value"]]

    return [
        INSTRUCTION_GROUPS["ALU"],
        ALU_OPERATIONS["LSHIFT"],
        alu_operands,
    ]


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably an LSHIFT assembly line, return an
    empty list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of instruction byte template dictionaries or an
        empty list.
    """

    match, signature = match_and_parse_line(
        line, _NAME, generate_signatures()
    )

    if not match:
        return []

    instruction_byte = instruction_byte_from_bitdefs(
        generate_instruction_byte_bitdefs(signature)
    )
    mc_byte = get_machine_code_byte_template()
    mc_byte["byte_type"] = "instruction"
    mc_byte["bitstring"] = instruction_byte

    return [mc_byte]

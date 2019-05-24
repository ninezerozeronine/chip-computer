"""
Template for operation module
"""

from ..language_defs import (
    INSTRUCTION_GROUPS,
    MODULE_CONTROL,
    ALU_OPERANDS,
    ALU_OPERATIONS,
    ALU_CONTROL_FLAGS,
    FLAGS,
    instruction_byte_from_bitdefs,
)
from ..operation_utils import assemble_instruction, match_and_parse_line
from ..data_structures import (
    get_arg_def_template, get_machine_code_byte_template
)

_NAME = "ADD"


def generate_microcode_templates():
    """
    Generate microcode for all the ADD instructions.

    Returns:
        list(DataTemplate): DataTemplates for all the ADD instructions.
    """

    data_templates = []

    signatures = generate_signatures()
    for signature in signatures:
        templates = generate_operation_templates(signature)
        data_templates.extend(templates)

    return data_templates


def generate_signatures():
    """
    Generate all the argument signatures for the ADD operation.

    Returns:
        list(list(dict)): All possible signatures, See
        :func:`~.get_arg_def_template` for more information on an
        argument definition dictionary.
    """

    signatures = []
    alu_args = ("ACC", "A", "B", "C")
    for alu_arg in alu_args:
        arg_def = get_arg_def_template()
        arg_def["value_type"] = "module_name"
        arg_def["value"] = alu_arg
        signatures.append([arg_def])

    return signatures


def generate_operation_templates(signature):
    """
    Create the DataTemplates to define a ADD with the given signature.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular ADD operation to generate
            templates for.
    Returns:
        list(DataTemplate) : DataTemplates that define this ADD.
    """

    instruction_byte_bitdefs = generate_instruction_byte_bitdefs(signature)

    flags_bitdefs = [FLAGS["ANY"]]

    control_steps = generate_control_steps(signature)

    return assemble_instruction(
        instruction_byte_bitdefs, flags_bitdefs, control_steps
    )


def generate_instruction_byte_bitdefs(signature):
    """
    Generate bitdefs to specify the instruction byte for this signature.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular ADD operation to generate
            the instruction byte bitdefs for.
    Returns:
        list(str): Bitdefs that make up the instruction_byte
    """

    return [
        INSTRUCTION_GROUPS["ALU"],
        ALU_OPERATIONS["ADD"],
        ALU_OPERANDS[signature[0]["value"]],
    ]


def generate_control_steps(signature):
    """
    Generate control steps for this signature.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular ADD operation to generate the
            control steps for.
    Returns:
        list(list(str)): List of list of bitdefs that specify the
        control steps.
    """

    step_0 = [
        MODULE_CONTROL[signature[0]["value"]]["OUT"],
        MODULE_CONTROL["ALU"]["STORE_RESULT"],
        MODULE_CONTROL["ALU"]["STORE_FLAGS"],
    ]
    step_0.extend(ALU_CONTROL_FLAGS["A_PLUS_B"])

    step_1 = [
        MODULE_CONTROL["ALU"]["OUT"],
        MODULE_CONTROL["ACC"]["IN"],
    ]

    return [step_0, step_1]


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a ADD assembly line, return an empty
    list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of machine code byte template dictionaries or
        an empty list.
    """

    match, signature = match_and_parse_line(
        line, _NAME, generate_signatures()
    )

    if not match:
        return []

    instruction_byte = instruction_byte_from_bitdefs(
        generate_instruction_byte_bitdefs(signature)
    )

    mc_bytes = []

    mc_byte = get_machine_code_byte_template()
    mc_byte["byte_type"] = "instruction"
    mc_byte["bitstring"] = instruction_byte
    mc_bytes.append(mc_byte)

    return mc_bytes

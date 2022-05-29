"""
The ADDC operation

Adds a value to the accumulator, adding an extra 1 if the overflow flag
is set.
"""

import copy

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


_NAME = "ADDC"

def generate_microcode_templates():
    """
    Generate microcode for the ADDC instruction.

    Returns:
        list(DataTemplate): DataTemplates for all the ADDC instructions.
    """

    data_templates = []

    signatures = generate_signatures()
    for signature in signatures:
        templates = generate_operation_templates(signature)
        data_templates.extend(templates)

    return data_templates


def generate_signatures():
    """
    Generate all the argument signatures for the ADDC operation.

    Returns:
        list(list(dict)): All possible signatures, See
        :func:`~.get_arg_def_template` for more information on an
        argument definition dictionary.
    """

    signatures = []
    alu_args = ("A", "B", "C")
    for alu_arg in alu_args:
        arg_def = get_arg_def_template()
        arg_def["value_type"] = "module_name"
        arg_def["is_memory_location"] = False
        arg_def["value"] = alu_arg
        signatures.append([arg_def])

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "constant"
    arg_def["is_memory_location"] = False
    signatures.append([arg_def])

    return signatures


def generate_operation_templates(signature):
    """
    Create the DataTemplates to define a ADDC with the given signature.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular ADDC operation to generate
            templates for.
    Returns:
        list(DataTemplate) : DataTemplates that define the operation
        with this signature.
    """

    data_templates = []

    instruction_byte_bitdefs = generate_instruction_byte_bitdefs(signature)

    initial_control_steps = get_calculation_control_steps(signature)

    data_templates.extend(
        generate_true_data_templates(
            instruction_byte_bitdefs, initial_control_steps
        )
    )

    data_templates.extend(
        generate_false_data_templates(
            instruction_byte_bitdefs, initial_control_steps
        )
    )

    return data_templates


def get_calculation_control_steps(signature):
    """
    Get control steps that calcuate the new value.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular ADDC operation to generate
            templates for.
    Returns:
        list(list(str)): List of list of bitdefs that specify the
        control steps.
    Raises:
        ValueError: When the signature's first argument type is not a
            module name or constant.
    """

    control_steps = []

    # If we're adding a module to ACC
    if signature[0]["value_type"] == "module_name":
        step_0 = [
            MODULE_CONTROL[signature[0]["value"]]["OUT"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        ]
        control_steps.append(step_0)

    # Else if we're adding a constant to ACC
    elif signature[0]["value_type"] == "constant":
        step_0 = [
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
        ]

        step_1 = [
            MODULE_CONTROL["RAM"]["SEL_PROG_MEM"],
            MODULE_CONTROL["RAM"]["OUT"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
            MODULE_CONTROL["PC"]["COUNT"],
        ]
        control_steps.append(step_0)
        control_steps.append(step_1)

    # Else something odd has happened
    else:
        raise ValueError("ADDC argument 0 is not a module name or constant")

    return control_steps

def generate_true_data_templates(
        instruction_byte_bitdefs, initial_control_steps
    ):
    """
    Create datatemplates for an ADDC where an extra bit is needed.

    Args:
        instruction_byte_bitdefs (list(str)): List of the bitdefs that
            make up the instruction byte.
        initial_control_steps (list(list(str))) : List of list of
            bitdefs that specify the control steps.
    Returns:
        list(DataTemplate): : List of DataTemplates that describe the
        ADDC for this signature when the carry flag is high.
    """

    initial_control_steps_copy = copy.deepcopy(initial_control_steps)
    initial_control_steps_copy[-1].extend(
        ALU_CONTROL_FLAGS["A_PLUS_B_PLUS_1"]
    )
    update_acc_control_step = [
        MODULE_CONTROL["ALU"]["OUT"],
        MODULE_CONTROL["ACC"]["IN"],
    ]

    control_steps = []
    control_steps.extend(initial_control_steps)
    control_steps.append(update_acc_control_step)

    return assemble_instruction(
        instruction_byte_bitdefs,
        [FLAGS["CARRY_BORROW"]["HIGH"]],
        control_steps
    )

def generate_false_data_templates(
        instruction_byte_bitdefs, initial_control_steps
    ):
    """
    Create datatemplates for an ADDC where an extra bit is not needed.

    Args:
        instruction_byte_bitdefs (list(str)): List of the bitdefs that
            make up the instruction byte.
        initial_control_steps (list(list(str))) : List of list of
            bitdefs that specify the control steps.
    Returns:
        list(DataTemplate): : List of DataTemplates that describe the
        ADDC for this signature when the carry flag is low.
    """

    initial_control_steps_copy = copy.deepcopy(initial_control_steps)
    initial_control_steps_copy[-1].extend(
        ALU_CONTROL_FLAGS["A_PLUS_B"]
    )
    update_acc_control_step = [
        MODULE_CONTROL["ALU"]["OUT"],
        MODULE_CONTROL["ACC"]["IN"],
    ]

    control_steps = []
    control_steps.extend(initial_control_steps_copy)
    control_steps.append(update_acc_control_step)

    return assemble_instruction(
        instruction_byte_bitdefs,
        [FLAGS["CARRY_BORROW"]["LOW"]],
        control_steps
    )

def generate_instruction_byte_bitdefs(signature):
    """
    Generate bitdefs to specify the instruction byte for this signature.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular simple ALU operation to generate
            the instruction byte bitdefs for.
    Returns:
        list(str): Bitdefs that make up the instruction_byte
    """

    if signature[0]["value_type"] == "module_name":
        bitdefs = [
            INSTRUCTION_GROUPS["ALU"],
            ALU_OPERATIONS["ADDC"],
            ALU_OPERANDS[signature[0]["value"]],
        ]
    elif signature[0]["value_type"] == "constant":
        bitdefs = [
            INSTRUCTION_GROUPS["ALU"],
            ALU_OPERATIONS["ADDC"],
            ALU_OPERANDS["ACC/CONST"],
        ]

    return bitdefs


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably an ADDC assembly line, return an empty
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

    if signature[0]["value_type"] == "constant":
        mc_byte = get_machine_code_byte_template()
        mc_byte["byte_type"] = "constant"
        mc_byte["constant"] = signature[0]["value"]
        mc_bytes.append(mc_byte)

    return mc_bytes

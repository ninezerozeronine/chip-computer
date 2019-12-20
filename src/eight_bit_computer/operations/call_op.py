"""
CALL Operation

Push the current program counter (i.e. the next instruction to be
executed) onto the stack, then set the program counter (i.e. jump) to
the value in the given argument (module or constant).
"""

from ..language_defs import (
    INSTRUCTION_GROUPS,
    SRC_REGISTERS,
    DEST_REGISTERS,
    MODULE_CONTROL,
    ALU_CONTROL_FLAGS,
    FLAGS,
    instruction_byte_from_bitdefs,
)
from ..operation_utils import assemble_instruction, match_and_parse_line
from ..data_structures import (
    get_arg_def_template, get_machine_code_byte_template
)

_NAME = "CALL"


def generate_microcode_templates():
    """
    Generate microcode for all the CALL instructions.

    Returns:
        list(DataTemplate): DataTemplates for all the CALL instructions.
    """

    data_templates = []

    signatures = generate_signatures()
    for signature in signatures:
        templates = generate_operation_templates(signature)
        data_templates.extend(templates)

    return data_templates


def generate_signatures():
    """
    Generate all the argument signatures for the CALL operation.

    Returns:
        list(list(dict)): All possible signatures, See
        :func:`~.get_arg_def_template` for more information on an
        argument definition dictionary.
    """

    signatures = []
    modules = ("ACC", "A", "B", "C",)

    for module in modules:
        arg_def = get_arg_def_template()
        arg_def["value_type"] = "module_name"
        arg_def["is_memory_location"] = False
        arg_def["value"] = module
        signatures.append([arg_def])

    return signatures


def generate_operation_templates(signature):
    """
    Create the DataTemplates to define a CALL with the given signature.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular CALL operation to generate
            templates for.
    Returns:
        list(DataTemplate) : Datatemplates that define this CALL.
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
            specify which particular CALL operation to generate
            the instruction byte bitdefs for.
    Returns:
        list(str): Bitdefs that make up the instruction_byte
    """

    return [
        INSTRUCTION_GROUPS["LOAD"],
        SRC_REGISTERS[signature[0]["value"]],
        DEST_REGISTERS["SP+/-"],
    ]


def generate_control_steps(signature):
    """
    Generate control steps for this signature.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular CALL operation to generate the
            control steps for.
    Returns:
        list(list(str)): List of list of bitdefs that specify the
        control steps.
    """

    decr_sp = [
        MODULE_CONTROL["SP"]["OUT"],
        MODULE_CONTROL["ALU"]["A_IS_BUS"],
        MODULE_CONTROL["ALU"]["STORE_RESULT"],
    ]
    decr_sp.extend(ALU_CONTROL_FLAGS["A_MINUS_1"])

    update_sp_set_mar = [
        MODULE_CONTROL["ALU"]["OUT"],
        MODULE_CONTROL["SP"]["IN"],
        MODULE_CONTROL["MAR"]["IN"],
    ]

    pc_onto_stack = [
        MODULE_CONTROL["PC"]["OUT"],
        MODULE_CONTROL["RAM"]["IN"],
    ]

    module_into_pc = [
        MODULE_CONTROL[signature[0]["value"]]["OUT"],
        MODULE_CONTROL["PC"]["IN"],
    ]

    return [
        decr_sp,
        update_sp_set_mar,
        pc_onto_stack,
        module_into_pc,
    ]


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a CALL assembly line, return an empty
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

    mc_byte = get_machine_code_byte_template()
    mc_byte["byte_type"] = "instruction"
    mc_byte["bitstring"] = instruction_byte

    return [mc_byte]

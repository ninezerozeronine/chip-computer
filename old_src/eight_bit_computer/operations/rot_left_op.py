"""
The ROT_LEFT operation.

Moves all the bits in the number one place to the left (most
significant side). If the most significant bit was a 1, then after the
rotation this is set back on the least significant side.

This operation will generate and store (clobber) ALU flags.
"""

from ..language_defs import (
    INSTRUCTION_GROUPS,
    MODULE_CONTROL,
    MODULE_CONTROLS_NONE,
    DEST_REGISTERS,
    SRC_REGISTERS,
    ALU_CONTROL_FLAGS,
    FLAGS,
    instruction_byte_from_bitdefs,
)

from ..operation_utils import assemble_instruction, match_and_parse_line
from ..data_structures import (
    get_arg_def_template, get_machine_code_byte_template
)

_NAME = "ROT_LEFT"


def generate_microcode_templates():
    """
    Generate microcode for all the ROT_LEFT operations.

    Returns:
        list(DataTemplate): DataTemplates for all the ROT_LEFT
        microcode.
    """

    data_templates = []

    signatures = generate_signatures()
    for signature in signatures:
        templates = generate_operation_templates(signature)
        data_templates.extend(templates)

    return data_templates


def generate_signatures():
    """
    Generate the definitions of all possible arguments passable.

    Returns:
        list(list(dict)): All possible arguments. See
        :func:`~.get_arg_def_template` for more information.
    """

    signatures = []
    # Add module arguments
    for dest in ("ACC", "A", "B", "C"):
        signature = []

        arg0_def = get_arg_def_template()
        arg0_def["value_type"] = "module_name"
        arg0_def["is_memory_location"] = False
        arg0_def["value"] = dest
        signature.append(arg0_def)

        signatures.append(signature)

    return signatures


def generate_operation_templates(signature):
    """
    Create the DataTemplates to define a ROT_LEFT with the given
    args.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular operation to generate
            templates for.
    Returns:
        list(DataTemplate) : Datatemplates that define this
        ROT_LEFT.
    """
    data_templates = []
    data_templates.extend(generate_no_carry_datatemplates(signature))
    data_templates.extend(generate_with_carry_datatemplates(signature))
    return data_templates


def generate_no_carry_datatemplates(signature):
    """
    Create DataTemplates to define a rottate left with no carry.

    This is the case where the most significant bit was a zero.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular operation to generate
            templates for.
    Returns:
        list(DataTemplate) : Datatemplates that define the "no carry
        half" of a ROT_LEFT operation.
    """

    control_steps = []

    lshift_step = [
        MODULE_CONTROL[signature[0]["value"]]["OUT"],
        MODULE_CONTROL["ALU"]["A_IS_BUS"],
        MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        MODULE_CONTROL["ALU"]["STORE_RESULT"],
    ]
    lshift_step.extend(ALU_CONTROL_FLAGS["A_PLUS_A"])
    control_steps.append(lshift_step)

    # This is so that the carry and no carry version of this instruction
    # take the same number of instruction cycles.
    rot_no_carry_step0 = [
        MODULE_CONTROLS_NONE,
    ]
    control_steps.append(rot_no_carry_step0)

    rot_no_carry_step1 = [
        MODULE_CONTROL["ALU"]["OUT"],
        MODULE_CONTROL[signature[0]["value"]]["IN"],
    ]
    control_steps.append(rot_no_carry_step1)

    instruction_byte_bitdefs = generate_instruction_byte_bitdefs(signature)
    flags_bitdefs = [FLAGS["CARRY_BORROW"]["LOW"]]

    return assemble_instruction(
        instruction_byte_bitdefs, flags_bitdefs, control_steps
    )


def generate_instruction_byte_bitdefs(signature):
    """
    Generate bitdefs to specify the instruction byte for these args.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular operation to generate
            the instruction byte bitdefs for.
    Returns:
        list(str): Bitdefs that make up the instruction_byte
    """

    src_map = {
        "ACC": SRC_REGISTERS["SP"],
        "A": SRC_REGISTERS["SP"],
        "B": SRC_REGISTERS["SP+/-"],
        "C": SRC_REGISTERS["CONST"],
    }

    dest_map = {
        "ACC": DEST_REGISTERS["SP+/-"],
        "A": DEST_REGISTERS["CONST"],
        "B": DEST_REGISTERS["ACC"],
        "C": DEST_REGISTERS["SP+/-"],
    }

    return [
        INSTRUCTION_GROUPS["STORE"],
        src_map[signature[0]["value"]],
        dest_map[signature[0]["value"]],
    ]


def generate_with_carry_datatemplates(signature):
    """
    Create DataTemplates to define a rottate left with a carry.

    This is the case where the most significant bit was a one.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular operation to generate
            templates for.
    Returns:
        list(DataTemplate) : Datatemplates that define the "carry half"
        of a ROT_LEFT operation.
    """

    control_steps = []

    lshift_step = [
        MODULE_CONTROL[signature[0]["value"]]["OUT"],
        MODULE_CONTROL["ALU"]["A_IS_BUS"],
        MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        MODULE_CONTROL["ALU"]["STORE_RESULT"],
    ]
    lshift_step.extend(ALU_CONTROL_FLAGS["A_PLUS_A"])
    control_steps.append(lshift_step)

    add_one_step = [
        MODULE_CONTROL["ALU"]["OUT"],
        MODULE_CONTROL["ALU"]["A_IS_BUS"],
        MODULE_CONTROL["ALU"]["STORE_RESULT"],
    ]
    add_one_step.extend(ALU_CONTROL_FLAGS["A_PLUS_1"])
    control_steps.append(add_one_step)

    write_back_step = [
        MODULE_CONTROL["ALU"]["OUT"],
        MODULE_CONTROL[signature[0]["value"]]["IN"],
    ]
    control_steps.append(write_back_step)

    instruction_byte_bitdefs = generate_instruction_byte_bitdefs(signature)
    flags_bitdefs = [FLAGS["CARRY_BORROW"]["HIGH"]]

    return assemble_instruction(
        instruction_byte_bitdefs, flags_bitdefs, control_steps
    )


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably an ROT_LEFT assembly line, return an
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

    instruction_byte_bitstring = instruction_byte_from_bitdefs(
        generate_instruction_byte_bitdefs(signature)
    )

    mc_bytes = []

    instruction_byte = get_machine_code_byte_template()
    instruction_byte["byte_type"] = "instruction"
    instruction_byte["bitstring"] = instruction_byte_bitstring
    mc_bytes.append(instruction_byte)

    return mc_bytes

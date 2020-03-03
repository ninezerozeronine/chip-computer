"""
The JUMP_IF_EQ_ZERO operation.

Sets PC (jumps) to a constant if the module passed as an argument is
equal to zero.

This operation will generate and store (clobber) ALU flags.
"""

from ..language_defs import (
    INSTRUCTION_GROUPS,
    MODULE_CONTROL,
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

_NAME = "JUMP_IF_EQ_ZERO"


def generate_microcode_templates():
    """
    Generate microcode for all the JUMP_IF_EQ_ZERO operations.

    Returns:
        list(DataTemplate): DataTemplates for all the JUMP_IF_EQ_ZERO
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
    for dest in ("ACC", "A", "B", "C", "PC", "SP"):
        signature = []

        arg0_def = get_arg_def_template()
        arg0_def["value_type"] = "module_name"
        arg0_def["is_memory_location"] = False
        arg0_def["value"] = dest
        signature.append(arg0_def)

        arg1_def = get_arg_def_template()
        arg1_def["value_type"] = "constant"
        arg1_def["is_memory_location"] = False
        signature.append(arg1_def)

        signatures.append(signature)

    return signatures


def generate_operation_templates(signature):
    """
    Create the DataTemplates to define a JUMP_IF_EQ_ZERO with the given
    args.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular operation to generate
            templates for.
    Returns:
        list(DataTemplate) : Datatemplates that define this
        JUMP_IF_EQ_ZERO.
    """
    data_templates = []
    data_templates.extend(generate_false_datatemplates(signature))
    data_templates.extend(generate_true_datatemplates(signature))
    return data_templates


def generate_false_datatemplates(signature):
    """
    Create DataTemplates to define a conditional jump if condition is
    false.

    This is the case where no jump happens.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular operation to generate
            templates for.
    Returns:
        list(DataTemplate) : Datatemplates that define the "false half"
        of the operation.
    """

    control_steps = generate_nonconditional_steps(signature)

    jump_step_0 = [
        MODULE_CONTROL["PC"]["COUNT"],
    ]
    control_steps.append(jump_step_0)

    instruction_byte_bitdefs = generate_instruction_byte_bitdefs(signature)
    flags_bitdefs = [FLAGS["ZERO"]["LOW"]]

    return assemble_instruction(
        instruction_byte_bitdefs, flags_bitdefs, control_steps
    )


def generate_nonconditional_steps(signature):
    """
    Generate the nonconditional control steps.

    These steps generate the flags which then govern whether the jump
    happens or not.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular operation to generate steps for.
    Returns:
        list(list(str)) : List of list of bitdefs that represent the
        steps, and the control signals at each step.
    """

    control_steps = []

    gen_flags_step_0 = [
        MODULE_CONTROL[signature[0]["value"]]["OUT"],
        MODULE_CONTROL["ALU"]["A_IS_BUS"],
        MODULE_CONTROL["ALU"]["STORE_FLAGS"],
    ]
    gen_flags_step_0.extend(ALU_CONTROL_FLAGS["A"])
    control_steps.append(gen_flags_step_0)

    return control_steps


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

    return [
        INSTRUCTION_GROUPS["STORE"],
        SRC_REGISTERS["SP"],
        DEST_REGISTERS[signature[0]["value"]],
    ]


def generate_true_datatemplates(signature):
    """
    Create DataTemplates to define a conditional jump if condition is true.

    This is the case where no jump happens

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular operation to generate
            templates for.
    Returns:
        list(DataTemplate) : Datatemplates that define the "true half"
        of a JUMP_IF_***_ACC operation.
    """

    control_steps = generate_nonconditional_steps(signature)

    # Now do the jump
    jump_step_0 = [
        MODULE_CONTROL["PC"]["OUT"],
        MODULE_CONTROL["MAR"]["IN"],
    ]
    control_steps.append(jump_step_0)

    jump_step_1 = [
        MODULE_CONTROL["RAM"]["SEL_PROG_MEM"],
        MODULE_CONTROL["RAM"]["OUT"],
        MODULE_CONTROL["PC"]["IN"],
    ]
    control_steps.append(jump_step_1)

    instruction_byte_bitdefs = generate_instruction_byte_bitdefs(signature)
    flags_bitdefs = [FLAGS["ZERO"]["HIGH"]]

    return assemble_instruction(
        instruction_byte_bitdefs, flags_bitdefs, control_steps
    )


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably an JUMP_IF_EQ_ZERO assembly line, return an
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

    jump_target_byte = get_machine_code_byte_template()
    jump_target_byte["byte_type"] = "constant"
    jump_target_byte["constant"] = signature[1]["value"]
    mc_bytes.append(jump_target_byte)

    return mc_bytes

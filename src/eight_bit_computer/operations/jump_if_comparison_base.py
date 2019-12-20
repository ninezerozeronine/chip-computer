"""
Base functionality for the the JUMP_IF_***_ACC operations.

Except JUMP_IF_EQ_ACC
"""

from itertools import product

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


def generate_microcode_templates(
    instruction_group,
    instruction_byte_const_bitdef,
    instruction_byte_arg_bitdef_dict,
    alu_flag_gen_bitdefs,
    true_flag_bitdefs,
    false_flag_bitdefs,
):
    """
    Generate microcode for this JUMP_IF_***_ACC operations.

    Args:
        instruction_group (str): Bitdef representing the instruction
            group for the instruction byte.
        instruction_byte_const_bitdef (str): Bitdef representing the
            part of the instruction byte that remains the same
            regardless of the arguments. Could be on the source side or
            the dest side.
        instruction_byte_arg_bitdef_map (dist(str:str)): Dictionary that
            contains the bitdefs which map to the arguments used. On the
            complementary side (i.e. src vs. dest) to the side used by
            the instruction_byte_const_bitdef.
        alu_flag_gen_bitdefs (list(str)): List of bitdefs that make up
            the control flags for the ALU to generate the appropriate
            flags.
        true_flag_bitdefs (list(str)): List of bitdef that represent the flag
            state when the condition is true.
        false_flag_bitdefs (list(str)): List of bitdef that represent the flag
            state when the condition is false.

    Returns:
        list(DataTemplate): DataTemplates for all the JUMP_IF_***_ACC
        microcode.
    """

    data_templates = []

    signatures = generate_signatures()
    for signature in signatures:
        templates = generate_operation_templates(
            signature,
            instruction_group,
            instruction_byte_const_bitdef,
            instruction_byte_arg_bitdef_dict,
            alu_flag_gen_bitdefs,
            true_flag_bitdefs,
            false_flag_bitdefs,
        )
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
    for dest in ("A", "B", "C", "PC", "SP"):
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

    # Add const argument
    const_signature = []

    const_arg0_def = get_arg_def_template()
    const_arg0_def["value_type"] = "constant"
    const_arg0_def["is_memory_location"] = False
    const_signature.append(const_arg0_def)

    const_arg1_def = get_arg_def_template()
    const_arg1_def["value_type"] = "constant"
    const_arg1_def["is_memory_location"] = False
    const_signature.append(const_arg1_def)

    signatures.append(const_signature)

    return signatures


def generate_operation_templates(
    signature,
    instruction_group,
    instruction_byte_const_bitdef,
    instruction_byte_arg_bitdef_dict,
    alu_flag_gen_bitdefs,
    true_flag_bitdefs,
    false_flag_bitdefs,
):
    """
    Create the DataTemplates to define a JUMP_IF_***_ACC with the given
    args.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular operation to generate
            templates for.
        instruction_group (str): Bitdef representing the instruction
            group for the instruction byte.
        instruction_byte_const_bitdef (str): Bitdef representing the
            part of the instruction byte that remains the same
            regardless of the arguments. Could be on the source side or
            the dest side.
        instruction_byte_arg_bitdef_map (dist(str:str)): Dictionary that
            contains the bitdefs which map to the arguments used. On the
            complementary side (i.e. src vs. dest) to the side used by
            the instruction_byte_const_bitdef.
        alu_flag_gen_bitdefs (list(str)): List of bitdefs that make up
            the control flags for the ALU to generate the appropriate
            flags.
        true_flag_bitdefs (list(str)): List of bitdefs that represent
            the flag state when the condition is true.
        false_flag_bitdefs (list(str)): List of bitdefs that represent
            the flag state when the condition is false.
    Returns:
        list(DataTemplate) : Datatemplates that define this
        JUMP_IF_***_ACC operation.
    """
    data_templates = []
    data_templates.extend(
        generate_false_datatemplates(
            signature,
            instruction_group,
            instruction_byte_const_bitdef,
            instruction_byte_arg_bitdef_dict,
            alu_flag_gen_bitdefs,
            false_flag_bitdefs,
        )
    )
    data_templates.extend(
        generate_true_datatemplates(
            signature,
            instruction_group,
            instruction_byte_const_bitdef,
            instruction_byte_arg_bitdef_dict,
            alu_flag_gen_bitdefs,
            true_flag_bitdefs,
        )
    )
    return data_templates


def generate_false_datatemplates(
    signature,
    instruction_group,
    instruction_byte_const_bitdef,
    instruction_byte_arg_bitdef_dict,
    alu_flag_gen_bitdefs,
    flag_bitdefs,
):
    """
    Create DataTemplates to define a conditional jump if condition is false.

    This is the case where no jump happens.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular not operation to generate
            templates for.
        instruction_group (str): Bitdef representing the instruction
            group for the instruction byte.
        instruction_byte_const_bitdef (str): Bitdef representing the
            part of the instruction byte that remains the same
            regardless of the arguments. Could be on the source side or
            the dest side.
        instruction_byte_arg_bitdef_map (dist(str:str)): Dictionary that
            contains the bitdefs which map to the arguments used. On the
            complementary side (i.e. src vs. dest) to the side used by
            the instruction_byte_const_bitdef.
        alu_flag_gen_bitdefs (list(str)): List of bitdefs that make up
            the control flags for the ALU to generate the appropriate
            flags.
        flag_bitdefs (list(str)): List of bitdef that represent the flag
            state when the condition is false.
    Returns:
        list(DataTemplate) : Datatemplates that define the "false half"
        of a JUMP_IF_***_ACC operation.
    """

    control_steps = generate_nonconditional_steps(
        signature, alu_flag_gen_bitdefs
    )

    if signature[0]["value_type"] == "constant":

        jump_step_0 = [
            MODULE_CONTROL["PC"]["COUNT"],
        ]
        control_steps.append(jump_step_0)

        jump_step_1 = [
            MODULE_CONTROL["PC"]["COUNT"],
        ]
        control_steps.append(jump_step_1)

    else:
        jump_step_0 = [
            MODULE_CONTROL["PC"]["COUNT"],
        ]
        control_steps.append(jump_step_0)

    instruction_byte_bitdefs = generate_instruction_byte_bitdefs(
        signature,
        instruction_group,
        instruction_byte_const_bitdef,
        instruction_byte_arg_bitdef_dict,
        )

    return assemble_instruction(
        instruction_byte_bitdefs, flag_bitdefs, control_steps
    )


def generate_nonconditional_steps(signature, alu_flag_gen_bitdefs):
    """
    Generate the nonconditional control steps.

    These steps generate the flags which then govern whether the jump
    happens or not.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular operation to generate steps for.
        alu_flag_gen_bitdefs (list(str)): List of bitdefs that make up
            the control flags for the ALU to generate the appropriate
            flags.
    Returns:
        list(list(str)) : List of list of bitdefs that represent the
        steps, and the control signals at each step.
    """

    control_steps = []

    if signature[0]["value_type"] == "constant":
        gen_flags_step_0 = [
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
        ]
        control_steps.append(gen_flags_step_0)

        gen_flags_step_1 = [
            MODULE_CONTROL["RAM"]["SEL_PROG_MEM"],
            MODULE_CONTROL["RAM"]["OUT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
            MODULE_CONTROL["PC"]["COUNT"],
        ]
        gen_flags_step_1.extend(alu_flag_gen_bitdefs)
        control_steps.append(gen_flags_step_1)

    else:
        gen_flags_step_0 = [
            MODULE_CONTROL[signature[0]["value"]]["OUT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
            MODULE_CONTROL["PC"]["COUNT"],
        ]
        gen_flags_step_0.extend(alu_flag_gen_bitdefs)
        control_steps.append(gen_flags_step_0)

    return control_steps


def generate_instruction_byte_bitdefs(
    signature,
    instruction_group,
    instruction_byte_const_bitdef,
    instruction_byte_arg_bitdef_dict,
):
    """
    Generate bitdefs to specify the instruction byte for these args.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular operation to generate
            the instruction byte bitdefs for.
        instruction_group (str): Bitdef representing the instruction
            group for the instruction byte.
        instruction_byte_const_bitdef (str): Bitdef representing the
            part of the instruction byte that remains the same
            regardless of the arguments. Could be on the source side or
            the dest side.
        instruction_byte_arg_bitdef_map (dist(str:str)): Dictionary that
            contains the bitdefs which map to the arguments used. On the
            complementary side (i.e. src vs. dest) to the side used by
            the instruction_byte_const_bitdef.
    Returns:
        list(str): Bitdefs that make up the instruction_byte
    """

    if signature[0]["value_type"] == "constant":
        arg_bitdef = instruction_byte_arg_bitdef_dict["CONST"]
    else:
        arg_bitdef = instruction_byte_arg_bitdef_dict[signature[0]["value"]]

    return [
        instruction_group,
        arg_bitdef,
        instruction_byte_const_bitdef
    ]


def generate_true_datatemplates(
    signature,
    instruction_group,
    instruction_byte_const_bitdef,
    instruction_byte_arg_bitdef_dict,
    alu_flag_gen_bitdefs,
    flag_bitdefs
):
    """
    Create DataTemplates to define a conditional jump if condition is true.

    This is the case where no jump happens

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular operation to generate
            templates for.
        instruction_group (str): Bitdef representing the instruction
            group for the instruction byte.
        instruction_byte_const_bitdef (str): Bitdef representing the
            part of the instruction byte that remains the same
            regardless of the arguments. Could be on the source side or
            the dest side.
        instruction_byte_arg_bitdef_map (dist(str:str)): Dictionary that
            contains the bitdefs which map to the arguments used. On the
            complementary side (i.e. src vs. dest) to the side used by
            the instruction_byte_const_bitdef.
        alu_flag_gen_bitdefs (list(str)): List of bitdefs that make up
            the control flags for the ALU to generate the appropriate
            flags.
        flag_bitdefs (list(str)): List of bitdef that represent the flag
            state when the condition is true.
    Returns:
        list(DataTemplate) : Datatemplates that define the "true half"
        of a JUMP_IF_***_ACC operation.
    """

    control_steps = generate_nonconditional_steps(
        signature, alu_flag_gen_bitdefs
    )

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

    instruction_byte_bitdefs = generate_instruction_byte_bitdefs(
        signature,
        instruction_group,
        instruction_byte_const_bitdef,
        instruction_byte_arg_bitdef_dict,
    )

    return assemble_instruction(
        instruction_byte_bitdefs, flag_bitdefs, control_steps
    )


def parse_line(
    line,
    name,
    instruction_group,
    instruction_byte_const_bitdef,
    instruction_byte_arg_bitdef_dict,
):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a JUMP_IF_***_ACC assembly line,
    return an empty list instead.

    Args:
        line (str): Assembly line to be parsed.
        name (str): Name of the operation. E.g. JUMP_IF_LT_ACC.
        instruction_group (str): Bitdef representing the instruction
            group for the instruction byte.
        instruction_byte_const_bitdef (str): Bitdef representing the
            part of the instruction byte that remains the same
            regardless of the arguments. Could be on the source side or
            the dest side.
        instruction_byte_arg_bitdef_map (dist(str:str)): Dictionary that
            contains the bitdefs which map to the arguments used. On the
            complementary side (i.e. src vs. dest) to the side used by
            the instruction_byte_const_bitdef.
    Returns:
        list(dict): List of instruction byte template dictionaries or an
        empty list.
    """

    match, signature = match_and_parse_line(
        line, name, generate_signatures()
    )

    if not match:
        return []

    instruction_byte_bitstring = instruction_byte_from_bitdefs(
        generate_instruction_byte_bitdefs(
            signature,
            instruction_group,
            instruction_byte_const_bitdef,
            instruction_byte_arg_bitdef_dict,
        )
    )

    mc_bytes = []

    instruction_byte = get_machine_code_byte_template()
    instruction_byte["byte_type"] = "instruction"
    instruction_byte["bitstring"] = instruction_byte_bitstring
    mc_bytes.append(instruction_byte)

    if signature[0]["value_type"] == "constant":
        const_comparison_byte = get_machine_code_byte_template()
        const_comparison_byte["byte_type"] = "constant"
        const_comparison_byte["constant"] = signature[0]["value"]
        mc_bytes.append(const_comparison_byte)

    jump_target_byte = get_machine_code_byte_template()
    jump_target_byte["byte_type"] = "constant"
    jump_target_byte["constant"] = signature[1]["value"]
    mc_bytes.append(jump_target_byte)

    return mc_bytes

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

    const_arg_def = get_arg_def_template()
    const_arg_def["value_type"] = "constant"
    const_arg_def["is_memory_location"] = False
    signatures.append([const_arg_def])

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

    instruction_byte_bitdefs = []
    instruction_byte_bitdefs.append(INSTRUCTION_GROUPS["LOAD"])
    instruction_byte_bitdefs.append(DEST_REGISTERS["SP+/-"])
    if signature[0]["value_type"] == "module_name":
        instruction_byte_bitdefs.append(SRC_REGISTERS[signature[0]["value"]])
    elif signature[0]["value_type"] == "constant":
        instruction_byte_bitdefs.append(SRC_REGISTERS["CONST"])

    return instruction_byte_bitdefs


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


    if signature[0]["value_type"] == "constant":
        sp_minus1_into_alu_incr_pc = [
            MODULE_CONTROL["SP"]["OUT"],
            MODULE_CONTROL["ALU"]["A_IS_BUS"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
            MODULE_CONTROL["PC"]["COUNT"],
        ]
        sp_minus1_into_alu_incr_pc.extend(ALU_CONTROL_FLAGS["A_MINUS_1"])

        alu_into_mar_and_sp = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["SP"]["IN"],
            MODULE_CONTROL["MAR"]["IN"],
        ]

        pc_into_data_ram_at_sp = [
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["RAM"]["IN"],
            MODULE_CONTROL["RAM"]["SEL_DATA_MEM"],
        ]

        pc_minus1_into_alu = [
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["ALU"]["A_IS_BUS"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
        ]
        pc_minus1_into_alu.extend(ALU_CONTROL_FLAGS["A_MINUS_1"])

        alu_into_mar = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
        ]

        constant_from_prog_to_pc = [
            MODULE_CONTROL["RAM"]["OUT"],
            MODULE_CONTROL["RAM"]["SEL_PROG_MEM"],
            MODULE_CONTROL["PC"]["IN"],
        ]

        return [
            sp_minus1_into_alu_incr_pc,
            alu_into_mar_and_sp,
            pc_into_data_ram_at_sp,
            pc_minus1_into_alu,
            alu_into_mar,
            constant_from_prog_to_pc,
        ]

    elif signature[0]["value_type"] == "module_name":
        sp_minus1_into_alu = [
            MODULE_CONTROL["SP"]["OUT"],
            MODULE_CONTROL["ALU"]["A_IS_BUS"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
        ]
        sp_minus1_into_alu.extend(ALU_CONTROL_FLAGS["A_MINUS_1"])

        alu_into_mar_and_sp = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["SP"]["IN"],
            MODULE_CONTROL["MAR"]["IN"],
        ]

        pc_onto_stack = [
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["RAM"]["IN"],
            MODULE_CONTROL["RAM"]["SEL_DATA_MEM"],
        ]

        module_into_pc = [
            MODULE_CONTROL[signature[0]["value"]]["OUT"],
            MODULE_CONTROL["PC"]["IN"],
        ]

        return [
            sp_minus1_into_alu,
            alu_into_mar_and_sp,
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

    mc_bytes = []

    mc_byte = get_machine_code_byte_template()
    mc_byte["byte_type"] = "instruction"
    mc_byte["bitstring"] = instruction_byte
    mc_bytes.append(mc_byte)

    if signature[0]["value_type"] == "constant":
        const_byte = get_machine_code_byte_template()
        const_byte["byte_type"] = "constant"
        const_byte["constant"] = signature[0]["value"]
        mc_bytes.append(const_byte)

    return mc_bytes

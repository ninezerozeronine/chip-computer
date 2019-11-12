"""
The LSHIFTC operation.

Moves all the bits in the argument one place to the left (toward the
most significant bit) in place. If the carry flag is high, a 1 is added
in the rightmost (least significant bit) place. If the flag is low, the
rightmost place is left as 0.
"""

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

_NAME = "LSHIFTC"


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
    Generate microcode for all the LSHIFTC operations.

    Returns:
        list(DataTemplate): DataTemplates for all the LSHIFTC microcode.
    """

    data_templates = []

    signatures = generate_signatures()
    for signature in signatures:

        instruction_byte_bitdefs = generate_instruction_byte_bitdefs(signature)

        add_control_steps = generate_control_steps(signature, True)

        data_templates.extend(
            assemble_instruction(
                instruction_byte_bitdefs,
                [FLAGS["CARRY_BORROW"]["HIGH"]],
                add_control_steps
            )
        )

        no_add_control_steps = generate_control_steps(signature, False)

        data_templates.extend(
            assemble_instruction(
                instruction_byte_bitdefs,
                [FLAGS["CARRY_BORROW"]["LOW"]],
                no_add_control_steps
            )
        )

    return data_templates


def generate_control_steps(signature, add_1):
    """
    Generate the control steps for a given signature, adding 1 or not.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular not operation to generate
            the instruction byte bitdefs for.
        add_1 (bool): Whether or not the control steps should add 1
            to the shifted result.
    Returns:
        list(list(str)): List of list of control flags for the steps.
    """

    control_steps = []
    step_0 = [
        MODULE_CONTROL[signature[0]["value"]]["OUT"],
        MODULE_CONTROL["ALU"]["A_IS_BUS"],
        MODULE_CONTROL["ALU"]["STORE_RESULT"],
        MODULE_CONTROL["ALU"]["STORE_FLAGS"],
    ]

    if add_1:
        step_0.extend(ALU_CONTROL_FLAGS["A_PLUS_A_PLUS_1"])
    else:
        step_0.extend(ALU_CONTROL_FLAGS["A_PLUS_A"])

    step_1 = [
        MODULE_CONTROL["ALU"]["OUT"],
        MODULE_CONTROL[signature[0]["value"]]["IN"],
    ]
    control_steps = [step_0, step_1]

    return control_steps


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
        alu_operand = ALU_OPERANDS["ACC/CONST"]
    else:
        alu_operand = ALU_OPERANDS[signature[0]["value"]]

    return [
        INSTRUCTION_GROUPS["ALU"],
        ALU_OPERATIONS["LSHIFTC"],
        alu_operand,
    ]


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably an LSHIFTC assembly line, return an
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

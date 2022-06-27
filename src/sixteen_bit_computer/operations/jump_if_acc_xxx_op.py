"""
The JUMP_IF_ACC_EQ and JUMP_IF_ACC_NEQ operations.

Jumps to a location in memory if the given module or constant
is or isn't equal to the Accumulator
"""

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    JUMP_IF_ACC_EQ,
    JUMP_IF_ACC_NEQ,
    A,
    B,
    C,
    PC,
    SP,
    CONST
)
from .. import number_utils
from ..language_defs import (
    MODULE_CONTROL,
    FLAGS,
    ALU_CONTROL_FLAGS,
)
from . import utils

_SUPPORTED_SIGNATURES = (
    (JUMP_IF_ACC_EQ, A, CONST),
    (JUMP_IF_ACC_EQ, B, CONST),
    (JUMP_IF_ACC_EQ, C, CONST),
    (JUMP_IF_ACC_EQ, PC, CONST),
    (JUMP_IF_ACC_EQ, SP, CONST),
    (JUMP_IF_ACC_EQ, CONST, CONST),
    (JUMP_IF_ACC_NEQ, A, CONST),
    (JUMP_IF_ACC_NEQ, B, CONST),
    (JUMP_IF_ACC_NEQ, C, CONST),
    (JUMP_IF_ACC_NEQ, PC, CONST),
    (JUMP_IF_ACC_NEQ, SP, CONST),
    (JUMP_IF_ACC_NEQ, CONST, CONST),
)


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the JUMP_IF_ACC_XXX operations.

    Args:
        signature (Tuple(:mod:`Instruction component<.instruction_components>`)):
            The signature to check.
        const_tokens (list(Token)): The tokens that represent constant
            values in the instruction.
    Returns:
        list(Word): The machinecode for the given signature.
    """
    if signature not in _SUPPORTED_SIGNATURES:
        raise ValueError

    if signature[1] == CONST:
        return [
            Word(value=get_instruction_index(signature)),
            Word(const_token=const_tokens[0]),
            Word(const_token=const_tokens[1]),
        ]
    else:
        return [
            Word(value=get_instruction_index(signature)),
            Word(const_token=const_tokens[0]),
        ]


def generate_microcode_templates():
    """
    Generate microcode for the JUMP_IF_ACC_XXX operations.

    Returns:
        list(DataTemplate): DataTemplates for all the JUMP_IF_ACC_XXX microcode.
    """

    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:

        if signature[1] == CONST:
            data_templates.extend(compare_to_const_templates(signature))
        else:
            data_templates.extend(compare_to_module_templates(signature))

    return data_templates


def compare_to_const_templates(signature):
    """

    """
    microcode_defs = []

    # First unconditional step to put PC into MAR
    step_0_flags = [FLAGS["ANY"]]
    step_0_module_controls = [
        MODULE_CONTROL["PC"]["OUT"],
        MODULE_CONTROL["MAR"]["IN"],
    ]
    microcode_defs.append({
        "step": 0,
        "flags": step_0_flags,
        "module_controls": step_0_module_controls,
    })

    # Second Unconditional step to actually generate the flags
    step_1_flags = [FLAGS["ANY"]]
    step_1_module_controls = [
        MODULE_CONTROL["MEM"]["READ_FROM"],
        MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        MODULE_CONTROL["PC"]["COUNT"],
    ]
    step_1_module_controls.extend(ALU_CONTROL_FLAGS["COMPARE_LTE_GT_EQ"])
    microcode_defs.append({
        "step": 1,
        "flags": step_1_flags,
        "module_controls": step_1_module_controls,
    })

    # If true, do the jump
    # First step of jump
    if signature[0] == JUMP_IF_ACC_EQ:
        true_step_2_flags = [FLAGS["EQUAL"]["HIGH"]]
    else:
        true_step_2_flags = [FLAGS["EQUAL"]["LOW"]]
    true_step_2_module_controls = [
        MODULE_CONTROL["PC"]["OUT"],
        MODULE_CONTROL["MAR"]["IN"],
    ]
    microcode_defs.append({
        "step": 2,
        "flags": true_step_2_flags,
        "module_controls": true_step_2_module_controls,
    })

    # Second step of the jump
    true_step_3_flags = [FLAGS["ANY"]]
    true_step_3_module_controls = [
        MODULE_CONTROL["MEM"]["READ_FROM"],
        MODULE_CONTROL["PC"]["IN"],
        MODULE_CONTROL["CU"]["STEP_RESET"],
    ]
    microcode_defs.append({
        "step": 3,
        "flags": true_step_3_flags,
        "module_controls": true_step_3_module_controls,
    })

    # If false, don't do the jump
    if signature[0] == JUMP_IF_ACC_EQ:
        false_step_2_flags = [FLAGS["EQUAL"]["LOW"]]
    else:
        false_step_2_flags = [FLAGS["EQUAL"]["HIGH"]]
    false_step_2_module_controls = [
        MODULE_CONTROL["PC"]["COUNT"],
        MODULE_CONTROL["CU"]["STEP_RESET"],
    ]
    microcode_defs.append({
        "step": 2,
        "flags": false_step_2_flags,
        "module_controls": false_step_2_module_controls,
    })

    instr_index = get_instruction_index(signature)
    data_templates = utils.assemble_explicit_instruction_steps(
        instr_index, microcode_defs
    )

    return data_templates


def compare_to_module_templates(signature):
    microcode_defs = []

    # First unconditional step to generate flags
    step_0_flags = [FLAGS["ANY"]]
    step_0_module_controls = [
        MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
        MODULE_CONTROL["ALU"]["STORE_FLAGS"],
    ]
    step_0_module_controls.extend(ALU_CONTROL_FLAGS["COMPARE_LTE_GT_EQ"])
    microcode_defs.append({
        "step": 0,
        "flags": step_0_flags,
        "module_controls": step_0_module_controls,
    })

    # If true, do the jump
    # First step of jump
    if signature[0] == JUMP_IF_ACC_EQ:
        true_step_1_flags = [FLAGS["EQUAL"]["HIGH"]]
    else:
        true_step_1_flags = [FLAGS["EQUAL"]["LOW"]]
    true_step_1_module_controls = [
        MODULE_CONTROL["PC"]["OUT"],
        MODULE_CONTROL["MAR"]["IN"],
    ]
    microcode_defs.append({
        "step": 1,
        "flags": true_step_1_flags,
        "module_controls": true_step_1_module_controls,
    })

    # Second step of the jump
    true_step_2_flags = [FLAGS["ANY"]]
    true_step_2_module_controls = [
        MODULE_CONTROL["MEM"]["READ_FROM"],
        MODULE_CONTROL["PC"]["IN"],
        MODULE_CONTROL["CU"]["STEP_RESET"],
    ]
    microcode_defs.append({
        "step": 2,
        "flags": true_step_2_flags,
        "module_controls": true_step_2_module_controls,
    })

    # If false, don't do the jump
    if signature[0] == JUMP_IF_ACC_EQ:
        false_step_1_flags = [FLAGS["EQUAL"]["LOW"]]
    else:
        false_step_1_flags = [FLAGS["EQUAL"]["HIGH"]]
    false_step_1_module_controls = [
        MODULE_CONTROL["PC"]["COUNT"],
        MODULE_CONTROL["CU"]["STEP_RESET"],
    ]
    microcode_defs.append({
        "step": 1,
        "flags": false_step_1_flags,
        "module_controls": false_step_1_module_controls,
    })

    instr_index = get_instruction_index(signature)
    data_templates = utils.assemble_explicit_instruction_steps(
        instr_index, microcode_defs
    )

    return data_templates


def supports(signature):
    """
    Whether this operation provides a definition for the given signature.

    Args:
        signature (Tuple(:mod:`Instruction component<.instruction_components>`)):
            The signature to check.
    Returns:
        bool: Whether it's supported or not.
    """
    return signature in _SUPPORTED_SIGNATURES

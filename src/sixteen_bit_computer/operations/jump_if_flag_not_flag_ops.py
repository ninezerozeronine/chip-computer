"""
The JUMP_IF_<FLAG> and JUMP_IF_NOT_<FLAG> operations.

Jumps to a location in memory of the given module is not equal to zero
"""

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    JUMP_IF_NEGATIVE_FLAG,
    JUMP_IF_NOT_NEGATIVE_FLAG,
    JUMP_IF_CARRYBORROW_FLAG,
    JUMP_IF_NOT_CARRYBORROW_FLAG,
    JUMP_IF_EQUAL_FLAG,
    JUMP_IF_NOT_EQUAL_FLAG,
    JUMP_IF_ZERO_FLAG,
    JUMP_IF_NOT_ZERO_FLAG,
    CONST,
)
from .. import number_utils
from ..language_defs import (
    MODULE_CONTROL,
    FLAGS,
    ALU_CONTROL_FLAGS,
)
from . import utils

_SUPPORTED_SIGNATURES = (
    (JUMP_IF_NEGATIVE_FLAG, CONST),
    (JUMP_IF_NOT_NEGATIVE_FLAG, CONST),
    (JUMP_IF_CARRYBORROW_FLAG, CONST),
    (JUMP_IF_NOT_CARRYBORROW_FLAG, CONST),
    (JUMP_IF_EQUAL_FLAG, CONST),
    (JUMP_IF_NOT_EQUAL_FLAG, CONST),
    (JUMP_IF_ZERO_FLAG, CONST),
    (JUMP_IF_NOT_ZERO_FLAG, CONST),
)

_OPERATION_TO_FLAGS = {
    JUMP_IF_NEGATIVE_FLAG : {
        "true_flags":[FLAGS["NEGATIVE"]["HIGH"]],
        "false_flags":[FLAGS["NEGATIVE"]["LOW"]],
    },
    JUMP_IF_NOT_NEGATIVE_FLAG : {
        "true_flags":[FLAGS["NEGATIVE"]["LOW"]],
        "false_flags":[FLAGS["NEGATIVE"]["HIGH"]],
    },
    JUMP_IF_CARRYBORROW_FLAG : {
        "true_flags":[FLAGS["CARRY_BORROW"]["HIGH"]],
        "false_flags":[FLAGS["CARRY_BORROW"]["LOW"]],
    },
    JUMP_IF_NOT_CARRYBORROW_FLAG : {
        "true_flags":[FLAGS["CARRY_BORROW"]["LOW"]],
        "false_flags":[FLAGS["CARRY_BORROW"]["HIGH"]],
    },
    JUMP_IF_EQUAL_FLAG : {
        "true_flags":[FLAGS["EQUAL"]["HIGH"]],
        "false_flags":[FLAGS["EQUAL"]["LOW"]],
    },
    JUMP_IF_NOT_EQUAL_FLAG : {
        "true_flags":[FLAGS["EQUAL"]["LOW"]],
        "false_flags":[FLAGS["EQUAL"]["HIGH"]],
    },
    JUMP_IF_ZERO_FLAG : {
        "true_flags":[FLAGS["ZERO"]["HIGH"]],
        "false_flags":[FLAGS["ZERO"]["LOW"]],
    },
    JUMP_IF_NOT_ZERO_FLAG : {
        "true_flags":[FLAGS["ZERO"]["LOW"]],
        "false_flags":[FLAGS["ZERO"]["HIGH"]],
    },
}



def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the JUMP_IF_<FLAG> and
    JUMP_IF_NOT_<FLAG> operations.

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

    return [
        Word(value=get_instruction_index(signature)),
        Word(const_token=const_tokens[0]),
    ]


def generate_microcode_templates():
    """
    Generate microcode for the JUMP_IF_<FLAG> and
    JUMP_IF_NOT_<FLAG> operations.

    Returns:
        list(DataTemplate): DataTemplates for all the
        JUMP_IF_<FLAG> and JUMP_IF_NOT_<FLAG> microcode.
    """

    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:

        microcode_defs = []

        # If true, address memory with PC
        true_step_0_flags = _OPERATION_TO_FLAGS[signature[0]]["true_flags"]
        true_step_0_module_controls = [
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
        ]
        microcode_defs.append({
            "step": 0,
            "flags": true_step_0_flags,
            "module_controls": true_step_0_module_controls,
        })

        # Read from mem, write into PC
        true_step_1_flags = [FLAGS["ANY"]]
        true_step_1_module_controls = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["PC"]["IN"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": 1,
            "flags": true_step_1_flags,
            "module_controls": true_step_1_module_controls,
        })

        # If false, don't jump
        false_step_0_flags = _OPERATION_TO_FLAGS[signature[0]]["false_flags"]
        false_step_0_module_controls = [
            MODULE_CONTROL["PC"]["COUNT"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": 0,
            "flags": false_step_0_flags,
            "module_controls": false_step_0_module_controls,
        })

        instr_index = get_instruction_index(signature)
        data_templates.extend(utils.assemble_explicit_instruction_steps(
            instr_index, microcode_defs
        ))

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

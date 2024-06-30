"""
The ROT_LEFT operation.

Moves all the bits one place to the left (toward the MSB),
wrapping the last bit around to the start (the LSB).
"""

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    ROT_LEFT,
    ACC,
    A,
    B,
    C,
)
from .. import number_utils
from ..language_defs import (
    MODULE_CONTROL,
    FLAGS,
    ALU_CONTROL_FLAGS,
)
from . import utils

_SUPPORTED_SIGNATURES = (
    (ROT_LEFT, ACC),
    (ROT_LEFT, A),
    (ROT_LEFT, B),
    (ROT_LEFT, C),
)


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the ROT_LEFT instructions.

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
        Word(value=get_instruction_index(signature))
    ]


def generate_microcode_templates():
    """
    Generate microcode for the ROT_LEFT operation.

    Returns:
        list(DataTemplate): DataTemplates for all the ROT_LEFT
        microcode.
    """

    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:

        microcode_defs = []

        # First unconditional step to add the input to itself
        step_0_flags = [FLAGS["ANY"]]
        step_0_module_controls = [
            MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
            MODULE_CONTROL["ALU"]["A_IS_BUS"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
        ]
        step_0_module_controls.extend(ALU_CONTROL_FLAGS["A_PLUS_A"])
        microcode_defs.append({
            "step": 0,
            "flags": step_0_flags,
            "module_controls": step_0_module_controls,
        })

        # If the shift left overflowed, add one
        add_1_step_1_flags = [FLAGS["CARRY_BORROW"]["HIGH"]]
        add_1_step_1_module_controls = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["ALU"]["A_IS_BUS"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
        ]
        add_1_step_1_module_controls.extend(ALU_CONTROL_FLAGS["A_PLUS_1"])
        microcode_defs.append({
            "step": 1,
            "flags": add_1_step_1_flags,
            "module_controls": add_1_step_1_module_controls,
        })

        # Then write the result back into the original module
        add_1_step_2_flags = [FLAGS["ANY"]]
        add_1_step_2_module_controls = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL[utils.component_to_module_name(signature[1])]["IN"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": 2,
            "flags": add_1_step_2_flags,
            "module_controls": add_1_step_2_module_controls,
        })

        # If the shift left didnt overflow we're done, write the
        # result back into the original module
        no_add_1_step_1_flags = [FLAGS["CARRY_BORROW"]["LOW"]]
        no_add_1_step_1_module_controls = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL[utils.component_to_module_name(signature[1])]["IN"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": 1,
            "flags": no_add_1_step_1_flags,
            "module_controls": no_add_1_step_1_module_controls,
        })

        instr_index = get_instruction_index(signature)
        data_templates.extend(
            utils.assemble_explicit_instruction_steps(
                instr_index, microcode_defs
            )
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
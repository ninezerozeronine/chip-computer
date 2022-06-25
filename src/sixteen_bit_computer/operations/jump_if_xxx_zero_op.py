"""
The JUMP_IF_EQ_ZERO operation.

Jumps to a location in memory of the given module is not equal to zero
"""

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    JUMP_IF_EQ_ZERO,
    JUMP_IF_NEQ_ZERO,
    ACC,
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
    (JUMP_IF_EQ_ZERO, ACC, CONST),
    (JUMP_IF_EQ_ZERO, A, CONST),
    (JUMP_IF_EQ_ZERO, B, CONST),
    (JUMP_IF_EQ_ZERO, C, CONST),
    (JUMP_IF_EQ_ZERO, PC, CONST),
    (JUMP_IF_EQ_ZERO, SP, CONST),
    (JUMP_IF_NEQ_ZERO, ACC, CONST),
    (JUMP_IF_NEQ_ZERO, A, CONST),
    (JUMP_IF_NEQ_ZERO, B, CONST),
    (JUMP_IF_NEQ_ZERO, C, CONST),
    (JUMP_IF_NEQ_ZERO, PC, CONST),
    (JUMP_IF_NEQ_ZERO, SP, CONST),
)


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the JUMP_IF_EQ_ZERO instruction.

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
    Generate microcode for the JUMP_IF_EQ_ZERO operation.

    Returns:
        list(DataTemplate): DataTemplates for all the JUMP_IF_EQ_ZERO microcode.
    """

    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:

        microcode_defs = []

        # Unconditional first step to generate flags
        step = 0
        flags = [FLAGS["ANY"]]
        module_controls = [
            MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
            MODULE_CONTROL["ALU"]["A_IS_BUS"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        ]
        module_controls.extend(ALU_CONTROL_FLAGS["A"])
        microcode_defs.append({
            "step": step,
            "flags": flags,
            "module_controls": module_controls,
        })

        # If the zero flag was set, perform the jump.
        #
        # PC is currently pointing at the location in memory that holds the
        # location to jump to (this was the second instruction word).
        # Set the MAR with the value of PC so it can then be loaded from memory.
        step = 1
        if signature[0] == JUMP_IF_EQ_ZERO:
            flags = [FLAGS["ZERO"]["HIGH"]]
        elif signature[0] == JUMP_IF_NEQ_ZERO:
            flags = [FLAGS["ZERO"]["LOW"]]
        module_controls = [
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
        ]
        microcode_defs.append({
            "step": step,
            "flags": flags,
            "module_controls": module_controls,
        })

        # Next step of the jump.
        #
        # Set PC to the value of the second instruction word and reset the
        # microcode step to fetch the next instruction from that location.
        step = 2
        flags = [FLAGS["ANY"]]
        module_controls = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["PC"]["IN"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": step,
            "flags": flags,
            "module_controls": module_controls,
        })

        # If the zero flag wasn't set, increment the program counter to move past
        # the constant that would have been jumped to and reset the step counter.
        # to fetch the next instruction.
        step = 1
        if signature[0] == JUMP_IF_EQ_ZERO:
            flags = [FLAGS["ZERO"]["LOW"]]
        elif signature[0] == JUMP_IF_NEQ_ZERO:
            flags = [FLAGS["ZERO"]["HIGH"]]
        module_controls = [
            MODULE_CONTROL["PC"]["COUNT"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": step,
            "flags": flags,
            "module_controls": module_controls,
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

"""
The JUMP operation.

Starts execution at a given location
"""

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    JUMP,
    CONST,
    ACC,
    A,
    B,
    C,
    SP,
    M_ACC,
    M_A,
    M_B,
    M_C,
    M_SP,
    M_CONST,
    memory_ref_to_component
)
from .. import number_utils
from ..language_defs import (
    MODULE_CONTROL,
    FLAGS,
    ALU_CONTROL_FLAGS,
)
from . import utils

_SUPPORTED_SIGNATURES = (
    (JUMP, ACC),
    (JUMP, A),
    (JUMP, B),
    (JUMP, C),
    (JUMP, SP),
    (JUMP, CONST),
    (JUMP, M_ACC),
    (JUMP, M_A),
    (JUMP, M_B),
    (JUMP, M_C),
    (JUMP, M_SP),
    (JUMP, M_CONST),
)


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the JUMP instruction.

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

    if signature in ((JUMP, CONST), (JUMP, M_CONST)):
        return [
            Word(value=get_instruction_index(signature)),
            Word(const_token=const_tokens[0]),
        ]
    else:
        return [
            Word(value=get_instruction_index(signature))
        ]


def generate_microcode_templates():
    """
    Generate microcode for the JUMP operation.

    Returns:
        list(DataTemplate): DataTemplates for all the JUMP microcode.
    """
    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:
        instr_index = get_instruction_index(signature)
        instr_index_bitdef = number_utils.number_to_bitstring(
            instr_index, bit_width=8
        )
        flags_bitdefs = [FLAGS["ANY"]]
        if signature[1] == CONST:
            control_steps = [
                [
                    MODULE_CONTROL["PC"]["OUT"],
                    MODULE_CONTROL["MAR"]["IN"],
                ],
                [
                    MODULE_CONTROL["MEM"]["READ_FROM"],
                    MODULE_CONTROL["PC"]["IN"],
                ],
            ]
        elif signature[1] in (ACC, A, B, C, SP):
            control_steps = [
                [
                    MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
                    MODULE_CONTROL["PC"]["IN"],
                ],
            ]
        elif signature[1] in (M_ACC, M_A, M_B, M_C, M_SP):
            module = memory_ref_to_component(signature[1])
            control_steps = [
                [
                    MODULE_CONTROL[utils.component_to_module_name(module)]["OUT"],
                    MODULE_CONTROL["MAR"]["IN"],
                ],
                [
                    MODULE_CONTROL["MEM"]["READ_FROM"],
                    MODULE_CONTROL["PC"]["IN"],
                ],
            ]
        elif signature[1] == M_CONST:
            step_0 = [
                MODULE_CONTROL["PC"]["OUT"],
                MODULE_CONTROL["MAR"]["IN"],
            ]
            # Need to store the address in the ALU rather than going
            # directly into the MAR, otherwise memory will be read,
            # and the address in memory will be change at the same
            # time - which will likely cause clock sync issues.
            step_1 = [
                MODULE_CONTROL["MEM"]["READ_FROM"],
                MODULE_CONTROL["ALU"]["STORE_RESULT"],
                MODULE_CONTROL["ALU"]["A_IS_BUS"],
            ]
            step_1.extend(ALU_CONTROL_FLAGS["A"])
                
            step_2 = [
                MODULE_CONTROL["ALU"]["OUT"],
                MODULE_CONTROL["MAR"]["IN"],
            ]

            step_3 = [
                MODULE_CONTROL["MEM"]["READ_FROM"],
                MODULE_CONTROL["PC"]["IN"],
            ]

            control_steps = [step_0, step_1, step_2, step_3]

        templates = utils.assemble_instruction_steps(
            instr_index_bitdef, flags_bitdefs, control_steps
        )
        data_templates.extend(templates)

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
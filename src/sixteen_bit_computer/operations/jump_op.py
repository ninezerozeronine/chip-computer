"""
The JUMP operation.

Starts execution at a given location
"""

import textwrap

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    JUMP,
    CONST,
    ACC,
    A,
    B,
    C,
    M_ACC,
    M_A,
    M_B,
    M_C,
    M_SP,
    M_CONST,
    memory_ref_to_component,
    component_to_assembly,
)
from .. import number_utils
from ..language_defs import (
    MODULE_CONTROL,
    FLAGS,
)
from . import utils

_SUPPORTED_SIGNATURES = (
    (JUMP, ACC),
    (JUMP, A),
    (JUMP, B),
    (JUMP, C),
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
                    MODULE_CONTROL["MEM"]["READ_FROM"],
                    MODULE_CONTROL["PC"]["IN"],
                ],
            ]
        elif signature[1] in (ACC, A, B, C):
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
            control_steps = [
                [
                    MODULE_CONTROL["MEM"]["READ_FROM"],
                    MODULE_CONTROL["MAR"]["IN"],
                ],
                [
                    MODULE_CONTROL["MEM"]["READ_FROM"],
                    MODULE_CONTROL["PC"]["IN"],
                ]
            ]

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

def gen_test_assembly():
    """
    Generate assembly code that verifies the instructions work as expected.
    """

    test_assembly = """\
    ////////////////////////////////////////////////////////////////
    // JUMP
    ////////////////////////////////////////////////////////////////

    &jump_0
        SET ACC &jump_1
        JUMP ACC
        HALT

    &jump_1
        SET A &jump_2
        JUMP A
        HALT

    &jump_2
        SET B &jump_3
        JUMP B
        HALT

    &jump_3
        SET C &jump_5
        JUMP C
        HALT

    &jump_5
        JUMP &jump_6
        HALT

    $v_jump_0 &jump7
    &jump_6
        SET ACC $v_jump_0
        JUMP [ACC]
        HALT

    $v_jump_1 &jump8
    &jump7
        SET A $v_jump_1
        JUMP [A]
        HALT

    $v_jump_2 &jump9
    &jump8
        SET B $v_jump_2
        JUMP [B]
        HALT

    $v_jump_3 &jump11
    &jump9
        SET C $v_jump_3
        JUMP [C]
        HALT

    $v_jump_5 &jump_done
    &jump11
        JUMP [$v_jump_5]
        HALT

    &jump_done
        NOOP
    """
    
    return textwrap.dedent(test_assembly)


def gen_all_assembly():
    """
    Generate assembly lines for all the instructions this module supports.

    Returns:
        list(str): The assembly lines.
    """
    ret = []
    for signature in _SUPPORTED_SIGNATURES:
        ret.append(" ".join(
            [component_to_assembly(component) for component in signature]
        ))
    return ret

"""
The NOT operation.

Inverts all the bits of the given argument.
"""

import textwrap

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    NOT,
    ACC,
    A,
    B,
    C,
    M_CONST,
    component_to_assembly
)
from .. import number_utils
from ..language_defs import (
    MODULE_CONTROL,
    FLAGS,
    ALU_CONTROL_FLAGS,
)
from . import utils

_SUPPORTED_SIGNATURES = (
    (NOT, ACC),
    (NOT, A),
    (NOT, B),
    (NOT, C),
    (NOT, M_CONST)
)


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the NOT instructions.

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

    if signature == (NOT, M_CONST):
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
    Generate microcode for the NOT operation.

    Returns:
        list(DataTemplate): DataTemplates for all the NOT
        microcode.
    """
    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:
        instr_index = get_instruction_index(signature)
        instr_index_bitdef = number_utils.number_to_bitstring(
            instr_index, bit_width=8
        )
        flags_bitdefs = [FLAGS["ANY"]]

        if signature[1] in (ACC, A, B, C):
            step_0 = [
                MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
                MODULE_CONTROL["ALU"]["STORE_RESULT"],
                MODULE_CONTROL["ALU"]["STORE_FLAGS"],
                MODULE_CONTROL["ALU"]["A_IS_BUS"],
            ]
            step_0.extend(ALU_CONTROL_FLAGS["NOT_A"])

            step_1 = [
                MODULE_CONTROL["ALU"]["OUT"],
                MODULE_CONTROL[utils.component_to_module_name(signature[1])]["IN"],
            ]

            control_steps = [step_0, step_1]

        if signature[1] == M_CONST:
            address_mem_and_pc_count = [
                MODULE_CONTROL["MEM"]["READ_FROM"],
                MODULE_CONTROL["MAR"]["IN"],
                MODULE_CONTROL["PC"]["COUNT"]
            ]

            not_val_into_alu = [
                MODULE_CONTROL["MEM"]["READ_FROM"],
                MODULE_CONTROL["ALU"]["STORE_RESULT"],
                MODULE_CONTROL["ALU"]["STORE_FLAGS"],
                MODULE_CONTROL["ALU"]["A_IS_BUS"],
            ]
            not_val_into_alu.extend(ALU_CONTROL_FLAGS["NOT_A"])

            alu_into_mem = [
                MODULE_CONTROL["MEM"]["WRITE_TO"],
                MODULE_CONTROL["ALU"]["OUT"],
            ]

            control_steps = [
                address_mem_and_pc_count,
                not_val_into_alu,
                alu_into_mem,
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
        // NOT
        ////////////////////////////////////////////////////////////////

    &not_0
        SET ACC        #0b1001_0100_0011_1111
        NOT ACC
        JUMP_IF_ACC_EQ #0b0110_1011_1100_0000 &not_1
        HALT

    &not_1
        SET A   #0b1010_1010_0101_0101
        SET ACC #0b0101_0101_1010_1010
        NOT A
        JUMP_IF_ACC_EQ A &not_2
        HALT

    &not_2
        SET B   #0b1111_1111_1111_1111
        SET ACC #0b0000_0000_0000_0000
        NOT B
        JUMP_IF_ACC_EQ B &not_3
        HALT

    &not_3
        SET C   #0b0000_0000_0000_0000
        SET ACC #0b1111_1111_1111_1111
        NOT C
        JUMP_IF_ACC_EQ C &not4
        HALT

    $v_not_0 #0b1111_0000_0101_1010
    &not_4
        NOT [$v_not_0]
        LOAD [$v_not_0] ACC
        JUMP_IF_ACC_EQ #0b0000_1111_1010_0101 $not_done
        HALT

    &not_done
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

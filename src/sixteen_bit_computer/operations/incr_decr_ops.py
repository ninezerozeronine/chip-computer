"""
The INCR and DECR operations.

Increnent or decrement the given argument by 1.
"""

import textwrap

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    INCR,
    DECR,
    ACC,
    A,
    B,
    C,
    M_CONST,
    component_to_assembly,
)
from .. import number_utils
from ..language_defs import (
    MODULE_CONTROL,
    FLAGS,
    ALU_CONTROL_FLAGS,
)
from . import utils

_SUPPORTED_SIGNATURES = (
    (INCR, ACC),
    (INCR, A),
    (INCR, B),
    (INCR, C),
    (INCR, M_CONST),
    (DECR, ACC),
    (DECR, A),
    (DECR, B),
    (DECR, C),
    (DECR, M_CONST),
)


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the INCR and DECR instructions.

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

    if signature[1] == M_CONST:
        return [
            Word(value=get_instruction_index(signature)),
            Word(const_token=const_tokens[0])
        ]
    else:
        return [
            Word(value=get_instruction_index(signature))
        ]

def generate_microcode_templates():
    """
    Generate microcode for the INCR and DECR operations.

    Returns:
        list(DataTemplate): DataTemplates for all the INCR and DECR
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
            # Module +/- 1 into ALU
            modlue_pm_into_alu = [
                    MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
                    MODULE_CONTROL["ALU"]["STORE_RESULT"],
                    MODULE_CONTROL["ALU"]["STORE_FLAGS"],
                    MODULE_CONTROL["ALU"]["A_IS_BUS"],
            ]
            if signature[0] == INCR:
                modlue_pm_into_alu.extend(ALU_CONTROL_FLAGS["A_PLUS_1"])
            elif signature[0] == DECR:
                modlue_pm_into_alu.extend(ALU_CONTROL_FLAGS["A_MINUS_1"])
            else:
                raise RuntimeError(
                    "Unexpected signature {sig} in incr/decr "
                    "microcode generation".format(sig=signature)
                )
            
            # ALU back into module
            alu_into_module = [
                MODULE_CONTROL["ALU"]["OUT"],
                MODULE_CONTROL[utils.component_to_module_name(signature[1])]["IN"],
            ]

            control_steps = [modlue_pm_into_alu, alu_into_module]

            templates = utils.assemble_instruction_steps(
                instr_index_bitdef, flags_bitdefs, control_steps
            )
            data_templates.extend(templates)

        elif signature[1] == M_CONST:
            mem_into_MAR_pc_count = [
                MODULE_CONTROL["MEM"]["READ_FROM"],
                MODULE_CONTROL["MAR"]["IN"],
                MODULE_CONTROL["PC"]["COUNT"],
            ]

            mem_val_pm_into_alu = [
                MODULE_CONTROL["MEM"]["READ_FROM"],
                MODULE_CONTROL["ALU"]["STORE_RESULT"],
                MODULE_CONTROL["ALU"]["STORE_FLAGS"],
                MODULE_CONTROL["ALU"]["A_IS_BUS"],
            ]
            if signature[0] == INCR:
                mem_val_pm_into_alu.extend(ALU_CONTROL_FLAGS["A_PLUS_1"])
            elif signature[0] == DECR:
                mem_val_pm_into_alu.extend(ALU_CONTROL_FLAGS["A_MINUS_1"])
            else:
                raise RuntimeError(
                    "Unexpected signature {sig} in incr/decr "
                    "microcode generation".format(sig=signature)
                )

            alu_into_mem = [
                MODULE_CONTROL["MEM"]["WRITE_TO"],
                MODULE_CONTROL["ALU"]["OUT"],
            ]

            control_steps = [
                mem_into_MAR_pc_count,
                mem_val_pm_into_alu,
                alu_into_mem
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
        // INCR
        ////////////////////////////////////////////////////////////////

    // INCR ACC
    &incr_0
        SET ACC #32
        INCR ACC 
        JUMP_IF_ACC_EQ #33 &incr_1
        HALT

    // INCR A
    &incr_1
        SET ACC #-31
        SET A #-32
        INCR A
        JUMP_IF_ACC_EQ A &incr_2
        HALT

    // INCR B
    &incr_2
        SET ACC #256
        SET B #255
        INCR B
        JUMP_IF_ACC_EQ B &incr_3
        HALT

    // INCR C
    &incr_3
        SET ACC #0
        SET C #0xFFFF
        INCR C
        JUMP_IF_ACC_EQ C &incr_4
        HALT

    // INCR M_CONST
    $incr_const_1
    &incr_4
        SET [$incr_const_1] #35
        INCR [$incr_const_1]
        LOAD [$incr_const_1] ACC
        JUMP_IF_ACC_EQ #36 &incr_5
        HALT

    // INCR M_CONST (carry flag)
    $incr_const_2
    &incr_5
        SET [$incr_const_2] #0b1111_1111_1111_1111
        INCR [$incr_const_2]
        JUMP_IF_CARRY &decr_0
        HALT

        ////////////////////////////////////////////////////////////////
        // DECR
        ////////////////////////////////////////////////////////////////

    // DECR ACC
    &decr_0
        SET ACC #32
        DECR ACC 
        JUMP_IF_ACC_EQ #31 &decr_1
        HALT

    // DECR A
    &decr_1
        SET ACC #-33
        SET A #-32
        DECR A
        JUMP_IF_ACC_EQ A &decr_2
        HALT

    // DECR B
    &decr_2
        SET ACC #255
        SET B #256
        DECR B
        JUMP_IF_ACC_EQ B &decr_3
        HALT

    // DECR C
    &decr_3
        SET ACC #0xFFFF
        SET C #0
        DECR C
        JUMP_IF_ACC_EQ C &decr_4
        HALT

    // DECR M_CONST
    $decr_const_1
    &decr_4
        SET [$decr_const_1] #50
        DECR [$decr_const_1]
        LOAD [$decr_const_1] ACC
        JUMP_IF_ACC_EQ #49 &decr_5
        HALT

    // DECR M_CONST (borrow flag)
    $decr_const_2
    &decr_5
        SET [$decr_const_2] #0
        DECR [$decr_const_2]
        JUMP_IF_BORROW &decr_end
        HALT

    &decr_end
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
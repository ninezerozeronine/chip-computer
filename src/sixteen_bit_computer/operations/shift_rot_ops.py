"""
The shift and rotate operations

If the popped bit (the bit at the far left or right if shifting or
rotating in that direction) is a 1, the carry bit is set.
"""

import textwrap

from ..instruction_listings import get_instruction_index
from ..instruction_components import (
    ROT_LEFT,
    ROT_RIGHT,
    SHIFT_LEFT,
    SHIFT_RIGHT,
    ACC,
    A,
    B,
    C,
    M_CONST,
    component_to_assembly
)
from .. import number_utils
from . import utils
from ..data_structures import Word
from ..language_defs import (
    FLAGS,
    MODULE_CONTROL,
    ALU_CONTROL_FLAGS,
)


_SUPPORTED_SIGNATURES = (
    (ROT_LEFT, ACC),
    (ROT_LEFT, A),
    (ROT_LEFT, B),
    (ROT_LEFT, C),
    (ROT_LEFT, M_CONST),
    (ROT_RIGHT, ACC),
    (ROT_RIGHT, A),
    (ROT_RIGHT, B),
    (ROT_RIGHT, C),
    (ROT_RIGHT, M_CONST),
    (SHIFT_LEFT, ACC),
    (SHIFT_LEFT, A),
    (SHIFT_LEFT, B),
    (SHIFT_LEFT, C),
    (SHIFT_LEFT, M_CONST),
    (SHIFT_RIGHT, ACC),
    (SHIFT_RIGHT, A),
    (SHIFT_RIGHT, B),
    (SHIFT_RIGHT, C),
    (SHIFT_RIGHT, M_CONST),
)


def generate_machinecode(signature, const_tokens):
    if signature not in _SUPPORTED_SIGNATURES:
        raise ValueError

    if signature[1] in (ACC, A, B, C):
        return [
            Word(value=get_instruction_index(signature))
        ]

    if signature[1] == M_CONST:
        return [
            Word(value=get_instruction_index(signature)),
            Word(const_token=const_tokens[0]),
        ]


def generate_microcode_templates():
    microcode_templates = []
    for signature in _SUPPORTED_SIGNATURES:
        instr_index = get_instruction_index(signature)
        instr_index_bitdef = number_utils.number_to_bitstring(
            instr_index, bit_width=8
        )
        flags_bitdefs = [FLAGS["ANY"]]
        control_steps = _generate_control_steps(signature)
        templates = utils.assemble_instruction_steps(
            instr_index_bitdef, flags_bitdefs, control_steps
        )
        microcode_templates.extend(templates)
    return microcode_templates


_OPCODE_TO_MODULE_OP = {
    ROT_LEFT: "ROTL_OUT",
    ROT_RIGHT: "ROTR_OUT",
    SHIFT_LEFT: "SHL_OUT",
    SHIFT_RIGHT: "SHR_OUT"
}


def _generate_control_steps(signature):
    if signature[1] in (ACC, A, B, C):
        mod_into_shr = [
            MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
            MODULE_CONTROL["SHR"]["IN"],
        ]
        shr_into_mod = [
            MODULE_CONTROL["SHR"][_OPCODE_TO_MODULE_OP[signature[0]]],
            MODULE_CONTROL[utils.component_to_module_name(signature[1])]["IN"],
        ]
        gen_flags = [
            MODULE_CONTROL["SHR"]["POPPED_BIT_OUT"],
            MODULE_CONTROL["ALU"]["A_IS_BUS"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        ]
        gen_flags.extend(
            ALU_CONTROL_FLAGS["A_PLUS_1"]
        )
        return [mod_into_shr, shr_into_mod, gen_flags]
    
    elif signature[1] == M_CONST:
        address_mem_and_pc_count = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["MAR"]["IN"],
            MODULE_CONTROL["PC"]["COUNT"]
        ]
        mem_val_into_shr = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["SHR"]["IN"],
        ]
        shr_into_mem = [
            MODULE_CONTROL["SHR"][_OPCODE_TO_MODULE_OP[signature[0]]],
            MODULE_CONTROL["MEM"]["WRITE_TO"],
        ]
        gen_flags = [
            MODULE_CONTROL["SHR"]["POPPED_BIT_OUT"],
            MODULE_CONTROL["ALU"]["A_IS_BUS"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        ]
        gen_flags.extend(
            ALU_CONTROL_FLAGS["A_PLUS_1"]
        )
        return [
            address_mem_and_pc_count,
            mem_val_into_shr,
            shr_into_mem,
            gen_flags
        ]

    else:
        raise ValueError("Unexpected signature.")


def supports(signature):
    return signature in _SUPPORTED_SIGNATURES


def gen_test_assembly():
    """
    Generate assembly code that verifies the instructions work as expected.
    """

    test_assembly = """\
        ////////////////////////////////////////////////////////////////
        // ROT_LEFT
        ////////////////////////////////////////////////////////////////

        // ROT_LEFT ACC
        SET ACC #0b1000_0000_0100_0000
        ROT_LEFT ACC
        JUMP_IF_ACC_EQ #0b0000_0000_1000_0001 &rot_left_0
        HALT

    &rot_left_0
        // ROT_LEFT A
        SET A #0b1111_0000_1111_0000
        ROT_LEFT A
        SET ACC #0b1110_0001_1110_0001
        JUMP_IF_ACC_EQ A &rot_left_1
        HALT

    &rot_left_1
        // ROT_LEFT B
        SET B #0b0000_0000_1111_0000
        ROT_LEFT B
        SET ACC #0b0000_0001_1110_0000
        JUMP_IF_ACC_EQ B &rot_left_2
        HALT

    &rot_left_2
        // ROT_LEFT C
        SET C #0b1111_1111_1111_1110
        ROT_LEFT C
        SET ACC #0b1111_1111_1111_1101
        JUMP_IF_ACC_EQ C &rot_left_3
        HALT

    $v_rot_left_0
    &rot_left_3
        // ROT_LEFT M_CONST
        SET [$v_rot_left_0] #0b0101_0101_1010_1010
        ROT_LEFT [$v_rot_left_0]
        LOAD [$v_rot_left_0] ACC
        JUMP_IF_ACC_EQ #0b1010_1011_0101_0100 &rot_left_4
        HALT
    
    &rot_left_4
        // ROT_LEFT ACC (with carry)
        SET ACC #0b1000_0000_0000_0000
        ROT_LEFT ACC
        JUMP_IF_CARRY &rot_left_5
        HALT
    
    &rot_left_5
        // ROT_LEFT ACC (no carry)
        SET ACC #0b0111_0000_0000_0000
        ROT_LEFT ACC
        JUMP_IF_NOT_CARRY &rot_right_0
        HALT

        ////////////////////////////////////////////////////////////////
        // ROT_RIGHT
        ////////////////////////////////////////////////////////////////

    &rot_right_0
        // ROT_RIGHT ACC
        SET ACC #0b1000_0000_0100_0001
        ROT_RIGHT ACC
        JUMP_IF_ACC_EQ #0b1100_0000_0010_0000 &rot_right_1
        HALT

    &rot_right_1
        // ROT_RIGHT A
        SET A #0b1111_0000_1111_0001
        ROT_RIGHT A
        SET ACC #0b1111_1000_0111_1000
        JUMP_IF_ACC_EQ A &rot_right_2
        HALT

    &rot_right_2
        // ROT_RIGHT B
        SET B #0b1111_0000_1111_0000
        ROT_RIGHT B
        SET ACC #0b0111_1000_0111_1000
        JUMP_IF_ACC_EQ B &rot_right_3
        HALT

    &rot_right_3
        // ROT_RIGHT C
        SET C #0b1111_1111_1111_1111
        ROT_RIGHT C
        SET ACC #0b1111_1111_1111_1111
        JUMP_IF_ACC_EQ C &rot_right_4
        HALT

    $v_rot_right_0
    &rot_right_4
        // ROT_RIGHT M_CONST
        SET [$v_rot_right_0] #0b0101_0101_1010_1010
        ROT_RIGHT [$v_rot_right_0]
        LOAD [$v_rot_right_0] ACC
        JUMP_IF_ACC_EQ #0b0010_1010_1101_0101 &rot_right_5
        HALT
        
    &rot_right_5
        // ROT_RIGHT ACC (with carry)
        SET ACC #0b0000_0000_0000_0001
        ROT_RIGHT ACC
        JUMP_IF_CARRY &rot_right_6
        HALT

    &rot_right_6
        // ROT_RIGHT ACC (no carry)
        SET ACC #0b1111_1111_1111_1110
        ROT_RIGHT ACC
        JUMP_IF_NOT_CARRY &shift_left_0
        HALT

        ////////////////////////////////////////////////////////////////
        // SHIFT_LEFT
        ////////////////////////////////////////////////////////////////

    &shift_left_0
        // SHIFT_LEFT ACC
        SET ACC #0b1010_0000_0100_0000
        SHIFT_LEFT ACC
        JUMP_IF_ACC_EQ #0b0100_0000_1000_0000 &shift_left_1
        HALT

    &shift_left_1
        // SHIFT_LEFT A
        SET A #0b1111_0000_1111_0010
        SHIFT_LEFT A
        SET ACC #0b1110_0001_1110_0100
        JUMP_IF_ACC_EQ A &shift_left_2
        HALT

    &shift_left_2
        // SHIFT_LEFT B
        SET B #0b1111_0000_1111_0010
        SHIFT_LEFT B
        SET ACC #0b1110_0001_1110_0100
        JUMP_IF_ACC_EQ B &shift_left_3
        HALT

    &shift_left_3
        // SHIFT_LEFT C
        SET C #0b0000_0101_1111_1111
        SHIFT_LEFT C
        SET ACC #0b0000_1011_1111_1110
        JUMP_IF_ACC_EQ C &shift_left_4
        HALT

    $v_shift_left_0
    &shift_left_4
        // SHIFT_LEFT M_CONST
        SET [$v_shift_left_0] #0b0101_0101_1010_1010
        SHIFT_LEFT [$v_shift_left_0]
        LOAD [$v_shift_left_0] ACC
        JUMP_IF_ACC_EQ #0b1010_1011_0101_0100 &shift_left_5
        HALT

    &shift_left_5
        // SHIFT_LEFT ACC (with carry)
        SET ACC #0b1000_0000_0000_0000
        SHIFT_LEFT ACC
        JUMP_IF_CARRY &shift_left_6
        HALT
    
    &shift_left_6
        // SHIFT_LEFT ACC (no carry)
        SET ACC #0b0111_0000_0000_0000
        SHIFT_LEFT ACC
        JUMP_IF_NOT_CARRY &shift_right_0
        HALT

        ////////////////////////////////////////////////////////////////
        // SHIFT_RIGHT
        ////////////////////////////////////////////////////////////////

    &shift_right_0
        // SHIFT_RIGHT ACC
        SET ACC #0b1010_0000_0100_0000
        SHIFT_RIGHT ACC
        JUMP_IF_ACC_EQ #0b0101_0000_0010_0000 &shift_right_1
        HALT

    &shift_right_1
        // SHIFT_RIGHT A
        SET A #0b1111_0000_1111_0010
        SHIFT_RIGHT A
        SET ACC #0b0111_1000_0111_1001
        JUMP_IF_ACC_EQ A &shift_right_2
        HALT

    &shift_right_2
        // SHIFT_RIGHT B
        SET B #0b1111_0000_1111_0010
        SHIFT_RIGHT B
        SET ACC #0b0111_1000_0111_1001
        JUMP_IF_ACC_EQ B &shift_right_3
        HALT

    &shift_right_3
        // SHIFT_RIGHT C
        SET C #0b0000_0101_1111_1111
        SHIFT_RIGHT C
        SET ACC #0b0000_0010_1111_1111
        JUMP_IF_ACC_EQ C &shift_right_4
        HALT

    $v_shift_right_0
    &shift_right_4
        // SHIFT_RIGHT M_CONST
        SET [$v_shift_right_0] #0b0101_0101_1010_1010
        SHIFT_RIGHT [$v_shift_right_0]
        LOAD [$v_shift_right_0] ACC
        JUMP_IF_ACC_EQ #0b0010_1010_1101_0101 &shift_right_5
        HALT

    &shift_right_5
        // SHIFT_RIGHT ACC (with carry)
        SET ACC #0b0000_0000_0000_0001
        SHIFT_RIGHT ACC
        JUMP_IF_CARRY &shift_right_6
        HALT
    
    &shift_right_6
        // SHIFT_RIGHT ACC (no carry)
        SET ACC #0b0000_0000_0000_0000
        SHIFT_RIGHT ACC
        JUMP_IF_NOT_CARRY &shift_right_done
        HALT

    &shift_right_done
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

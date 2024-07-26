"""
Copy operations
"""

import textwrap

from ..instruction_listings import get_instruction_index
from ..instruction_components import (
    COPY,
    ACC,
    A,
    B,
    C,
    X,
    Y,
    Z,
    PC,
    SP,
)
from .. import number_utils
from . import utils
from ..data_structures import Word
from ..language_defs import (
    FLAGS,
    MODULE_CONTROL,
)


_SUPPORTED_SIGNATURES = (
    (COPY, ACC, A),
    (COPY, ACC, B),
    (COPY, ACC, C),
    (COPY, ACC, SP),
    (COPY, ACC, X),
    (COPY, ACC, Y),
    (COPY, ACC, Z),
    (COPY, A, ACC),
    (COPY, A, B),
    (COPY, A, C),
    (COPY, B, ACC),
    (COPY, B, A),
    (COPY, B, C),
    (COPY, C, ACC),
    (COPY, C, A),
    (COPY, C, B),
    (COPY, X, ACC),
    (COPY, Y, ACC),
    (COPY, Z, ACC),
    (COPY, PC, ACC),
    (COPY, SP, ACC),
)


def generate_machinecode(signature, const_tokens):
    if signature not in _SUPPORTED_SIGNATURES:
        raise ValueError

    return [
        Word(value=get_instruction_index(signature))
    ]


def generate_microcode_templates():
    microcode_templates = []
    for signature in _SUPPORTED_SIGNATURES:
        instr_index = get_instruction_index(signature)
        instr_index_bitdef = number_utils.number_to_bitstring(
            instr_index, bit_width=8
        )
        flags_bitdefs = [FLAGS["ANY"]]

        control_steps = [
            [
                MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
                MODULE_CONTROL[utils.component_to_module_name(signature[2])]["IN"],
            ]
        ]
        templates = utils.assemble_instruction_steps(
            instr_index_bitdef, flags_bitdefs, control_steps
        )
        microcode_templates.extend(templates)
    return microcode_templates


def supports(signature):
    return signature in _SUPPORTED_SIGNATURES


def gen_test_assembly():
    test_assembly = """\
        ////////////////////////////////////////////////////////////////
        // COPY
        ////////////////////////////////////////////////////////////////

    &copy_0
        SET ACC #4799
        COPY ACC A
        JUMP_IF_ACC_EQ A &copy_1
        HALT

    &copy_1
        SET ACC #52686
        COPY ACC B
        JUMP_IF_ACC_EQ B &copy_2
        HALT

    &copy_2
        SET ACC #35304
        COPY ACC C
        JUMP_IF_ACC_EQ C &copy_3
        HALT

    &copy_3
        SET ACC #555
        COPY ACC SP
        SET_ZERO ACC
        COPY SP ACC
        JUMP_IF_ACC_EQ #555 &copy_4
        HALT

    &copy_4
        SET ACC #36
        SET A #36
        COPY ACC X
        SET_ZERO ACC
        COPY X ACC
        JUMP_IF_ACC_EQ A &copy_5
        HALT      

    &copy_5
        SET ACC #4456
        SET A #4456
        COPY ACC Y
        SET_ZERO ACC
        COPY Y ACC
        JUMP_IF_ACC_EQ A &copy_6
        HALT 

    &copy_7
        SET ACC #1234
        SET A #1234
        COPY ACC Z
        SET_ZERO ACC
        COPY Z ACC
        JUMP_IF_ACC_EQ A &copy_8
        HALT 

    &copy_8
        SET A #15993
        COPY A ACC
        JUMP_IF_ACC_EQ #15993 &copy_9
        HALT

    &copy_9
        SET A #28834
        SET ACC #28834
        COPY A B
        JUMP_IF_ACC_EQ B &copy_10
        HALT

    &copy_10
        SET A #58775
        SET ACC #58775
        COPY A C
        JUMP_IF_ACC_EQ C &copy_11
        HALT

    &copy_11
        SET C #48215
        COPY C ACC
        JUMP_IF_ACC_EQ #48215 &copy_12
        HALT

    &copy_12
        SET C #10020
        SET ACC #10020
        COPY C A
        JUMP_IF_ACC_EQ A &copy_13
        HALT

    &copy_13
        SET C #65463
        SET ACC #65463
        COPY C B
        JUMP_IF_ACC_EQ B &copy_14
        HALT

    &copy_13
        COPY PC ACC
    &pc_should_be_this
        JUMP_IF_ACC_EQ &pc_should_be_this &copy_end
        HALT
    
    &copy_end
        NOOP

    """

    return textwrap.dedent(test_assembly)
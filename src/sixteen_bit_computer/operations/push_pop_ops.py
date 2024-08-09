"""
The PUSH and POP operations.

PUSHing a value puts it onto the top of the stack and moves the stack
pointer to the next free space. POPing a value takes the value from
the top of the stack and moves the stack pointer to the now free
space.

The stack pointer always points at the item at the top of the stack.

The stack pointer gets a lower value/moves down in memory as you push
items onto the stack.

Initial State:

    0 <code>
    1 <code>
    2 
    3 34  <- SP
    4 12
    5 42
    6

    A:  55
    B:  77
    SP: 3


POP A:

    0 <code>
    1 <code>
    2 
    3 34  
    4 12 <- SP
    5 42
    6

    A:  34
    B:  77
    SP: 4

PUSH B

    0 <code>
    1 <code>
    2 
    3 77  <- SP
    4 12 
    5 42
    6

    A:  34
    B:  77
    SP: 3
"""

import textwrap

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    PUSH,
    POP,
    ACC,
    A,
    B,
    C,
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
    (PUSH, ACC),
    (PUSH, A),
    (PUSH, B),
    (PUSH, C),
    (POP, ACC),
    (POP, A),
    (POP, B),
    (POP, C),
)


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the PUSH and POP instructions.

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
    Generate microcode for the PUSH and POP operations.

    Returns:
        list(DataTemplate): DataTemplates for all the PUSH and POP
        microcode.
    """
    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:
        instr_index = get_instruction_index(signature)
        instr_index_bitdef = number_utils.number_to_bitstring(
            instr_index, bit_width=8
        )
        flags_bitdefs = [FLAGS["ANY"]]

        if signature[0] == PUSH:
            step_0 = [
                MODULE_CONTROL["SP"]["OUT"],
                MODULE_CONTROL["ALU"]["A_IS_BUS"],
                MODULE_CONTROL["ALU"]["STORE_RESULT"],
            ]
            step_0.extend(ALU_CONTROL_FLAGS["A_MINUS_1"])

            step_1 = [
                MODULE_CONTROL["ALU"]["OUT"],
                MODULE_CONTROL["SP"]["IN"],
                MODULE_CONTROL["MAR"]["IN"],
            ]

            step_2 = [
                MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
                MODULE_CONTROL["MEM"]["WRITE_TO"],
            ]

            control_steps = [step_0, step_1, step_2]

        elif signature[0] == POP:
            step_0 = [
                MODULE_CONTROL["SP"]["OUT"],
                MODULE_CONTROL["MAR"]["IN"],
                MODULE_CONTROL["ALU"]["A_IS_BUS"],
                MODULE_CONTROL["ALU"]["STORE_RESULT"],
            ]
            step_0.extend(ALU_CONTROL_FLAGS["A_PLUS_1"])

            step_1 = [
                MODULE_CONTROL["MEM"]["READ_FROM"],
                MODULE_CONTROL[utils.component_to_module_name(signature[1])]["IN"],
            ]

            step_2 = [
                MODULE_CONTROL["ALU"]["OUT"],
                MODULE_CONTROL["SP"]["IN"],
            ]

            control_steps = [step_0, step_1, step_2]
        else:
            raise RuntimeError(
                "Unexpected signature {sig} in load/store "
                "microcode generation".format(sig=signature)
            )

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
        // PUSH
        ////////////////////////////////////////////////////////////////

    &push_0
        NOOP
        NOOP
        NOOP
    &push_1
        NOOP
        NOOP
        NOOP
        SET SP &push_1    

        SET ACC #567
        PUSH ACC
        SET_ZERO ACC
        LOAD [SP] ACC
        JUMP_IF_ACC_EQ #567 &push_2
        HALT

    &push_2
        SET SP &push_1 
        SET A #123
        PUSH A
        LOAD [SP] ACC
        JUMP_IF_ACC_EQ #123 &push_3
        HALT

    &push_3
        SET SP &push_1 
        SET B #333
        PUSH B
        LOAD [SP] ACC
        JUMP_IF_ACC_EQ #333 &push_4
        HALT

    &push_4
        SET SP &push_1 
        SET C #22341
        PUSH C
        LOAD [SP] ACC
        JUMP_IF_ACC_EQ #22341 &pop_0
        HALT

        ////////////////////////////////////////////////////////////////
        // POP
        ////////////////////////////////////////////////////////////////

    &pop_0
        NOOP
        NOOP
    &pop_1
        NOOP
        NOOP
        NOOP
        SET SP &pop_1    

        SET ACC #6381
        PUSH ACC
        SET_ZERO ACC
        LOAD [SP] ACC
        JUMP_IF_ACC_EQ #6381 &pop_2
        HALT

    &pop_2
        SET SP &pop_1 
        SET A #5681
        PUSH A
        LOAD [SP] ACC
        JUMP_IF_ACC_EQ #5681 &pop_3
        HALT

    &pop_3
        SET SP &pop_1 
        SET B #22222
        PUSH B
        LOAD [SP] ACC
        JUMP_IF_ACC_EQ #22222 &pop_4
        HALT

    &pop_4
        SET SP &pop_1 
        SET C #4242
        PUSH C
        LOAD [SP] ACC
        JUMP_IF_ACC_EQ #4242 &pop_done
        HALT
    
    &pop_done
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

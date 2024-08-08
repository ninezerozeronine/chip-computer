"""
The JUMP_IF_EQ_ZERO  and JUMP_IF_NEQ_ZERO operations.

Jumps to a location in memory of the given module is not equal to zero
"""

import textwrap

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    JUMP_IF_EQ_ZERO,
    JUMP_IF_NEQ_ZERO,
    ACC,
    A,
    B,
    C,
    CONST,
    component_to_assembly,
)
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
    (JUMP_IF_NEQ_ZERO, ACC, CONST),
    (JUMP_IF_NEQ_ZERO, A, CONST),
    (JUMP_IF_NEQ_ZERO, B, CONST),
    (JUMP_IF_NEQ_ZERO, C, CONST),
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
    Generate microcode for the JUMP_IF_(N)EQ_ZERO operations.

    Returns:
        list(DataTemplate): DataTemplates for all the JUMP_IF_(N)EQ_ZERO microcode.
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
        step = 1
        if signature[0] == JUMP_IF_EQ_ZERO:
            flags = [FLAGS["ZERO"]["HIGH"]]
        elif signature[0] == JUMP_IF_NEQ_ZERO:
            flags = [FLAGS["ZERO"]["LOW"]]
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


def gen_test_assembly():
    """
    Generate assembly code that verifies the instructions work as expected.
    """

    test_assembly = """\
        ////////////////////////////////////////////////////////////////
        // JUMP_IF_EQ_ZERO
        ////////////////////////////////////////////////////////////////

    &jiez_0
        SET_ZERO ACC
        JUMP_IF_EQ_ZERO ACC &jiez_1
        HALT

    &jiez_1
        SET_ZERO A
        JUMP_IF_EQ_ZERO A &jiez_2
        HALT

    &jiez_2
        SET_ZERO B
        JUMP_IF_EQ_ZERO B &jiez_3
        HALT

    &jiez_3
        SET_ZERO C
        JUMP_IF_EQ_ZERO C &jiez_4
        HALT

    &jiez_4
        SET ACC #1
        JUMP_IF_EQ_ZERO ACC &jiez_halt_0

        SET A #58767
        JUMP_IF_EQ_ZERO A &jiez_halt_1

        SET B #443
        JUMP_IF_EQ_ZERO B &jiez_halt_2

        SET C #7687
        JUMP_IF_EQ_ZERO C &jiez_halt_3

        SET SP #1536
        JUMP_IF_EQ_ZERO SP &jiez_halt_4

        JUMP &jinez_0

    &jiez_halt_0
        NOOP
        NOOP
        HALT
        NOOP
        NOOP
    &jiez_halt_1
        NOOP
        NOOP
        HALT
        NOOP
        NOOP
    &jiez_halt_2
        NOOP
        NOOP
        HALT
        NOOP
        NOOP
    &jiez_halt_3
        NOOP
        NOOP
        HALT
        NOOP
        NOOP
    &jiez_halt_4
        NOOP
        NOOP
        HALT
        NOOP
        NOOP

        ////////////////////////////////////////////////////////////////
        // JUMP_IF_NEQ_ZERO
        ////////////////////////////////////////////////////////////////

    &jinez_0
        SET ACC #1
        JUMP_IF_NEQ_ZERO ACC &jinez_1
        HALT

    &jinez_1
        SET A #1
        JUMP_IF_NEQ_ZERO A &jinez_2
        HALT

    &jinez_2
        SET B #1
        JUMP_IF_NEQ_ZERO B &jinez_3
        HALT

    &jinez_3
        SET C #1
        JUMP_IF_NEQ_ZERO C &jinez_4
        HALT

    &jinez_4
        SET_ZERO ACC
        JUMP_IF_NEQ_ZERO ACC &jinez_halt_0

        SET_ZERO A
        JUMP_IF_NEQ_ZERO A &jinez_halt_1

        SET_ZERO B
        JUMP_IF_NEQ_ZERO B &jinez_halt_2

        SET_ZERO C
        JUMP_IF_NEQ_ZERO C &jinez_halt_3

        JUMP &jinez_done

    &jinez_halt_0
        NOOP
        NOOP
        HALT
        NOOP
        NOOP
    &jinez_halt_1
        NOOP
        NOOP
        HALT
        NOOP
        NOOP
    &jinez_halt_2
        NOOP
        NOOP
        HALT
        NOOP
        NOOP
    &jinez_halt_3
        NOOP
        NOOP
        HALT
        NOOP
        NOOP
    
    &jinez_done
        HALT
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
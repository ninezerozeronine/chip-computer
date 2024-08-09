"""
The JUMP_IF_<FLAG> and JUMP_IF_NOT_<FLAG> operations.

Jumps to a location in memory if the given flag is set (or not).
"""

import textwrap

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    JUMP_IF_NEGATIVE_FLAG,
    JUMP_IF_NOT_NEGATIVE_FLAG,
    JUMP_IF_CARRY,
    JUMP_IF_NOT_CARRY,
    JUMP_IF_BORROW,
    JUMP_IF_NOT_BORROW,
    JUMP_IF_EQUAL_FLAG,
    JUMP_IF_NOT_EQUAL_FLAG,
    JUMP_IF_ZERO_FLAG,
    JUMP_IF_NOT_ZERO_FLAG,
    CONST,
    component_to_assembly,
)
from ..language_defs import (
    MODULE_CONTROL,
    FLAGS,
)
from . import utils

_SUPPORTED_SIGNATURES = (
    (JUMP_IF_NEGATIVE_FLAG, CONST),
    (JUMP_IF_NOT_NEGATIVE_FLAG, CONST),
    (JUMP_IF_CARRY, CONST),
    (JUMP_IF_NOT_CARRY, CONST),
    (JUMP_IF_BORROW, CONST),
    (JUMP_IF_NOT_BORROW, CONST),
    (JUMP_IF_EQUAL_FLAG, CONST),
    (JUMP_IF_NOT_EQUAL_FLAG, CONST),
    (JUMP_IF_ZERO_FLAG, CONST),
    (JUMP_IF_NOT_ZERO_FLAG, CONST),
)

_OPERATION_TO_FLAGS = {
    JUMP_IF_NEGATIVE_FLAG : {
        "true_flags":[FLAGS["NEGATIVE"]["HIGH"]],
        "false_flags":[FLAGS["NEGATIVE"]["LOW"]],
    },
    JUMP_IF_NOT_NEGATIVE_FLAG : {
        "true_flags":[FLAGS["NEGATIVE"]["LOW"]],
        "false_flags":[FLAGS["NEGATIVE"]["HIGH"]],
    },
    JUMP_IF_CARRY:{
        "true_flags": [FLAGS["CARRY_BORROW"]["HIGH"]],
        "false_flags": [FLAGS["CARRY_BORROW"]["LOW"]],
    },
    JUMP_IF_NOT_CARRY:{
        "true_flags": [FLAGS["CARRY_BORROW"]["LOW"]],
        "false_flags": [FLAGS["CARRY_BORROW"]["HIGH"]],
    },
    JUMP_IF_BORROW:{
        "true_flags": [FLAGS["CARRY_BORROW"]["LOW"]],
        "false_flags": [FLAGS["CARRY_BORROW"]["HIGH"]],
    },
    JUMP_IF_NOT_BORROW:{
        "true_flags": [FLAGS["CARRY_BORROW"]["HIGH"]],
        "false_flags": [FLAGS["CARRY_BORROW"]["LOW"]],
    },
    JUMP_IF_EQUAL_FLAG : {
        "true_flags":[FLAGS["EQUAL"]["HIGH"]],
        "false_flags":[FLAGS["EQUAL"]["LOW"]],
    },
    JUMP_IF_NOT_EQUAL_FLAG : {
        "true_flags":[FLAGS["EQUAL"]["LOW"]],
        "false_flags":[FLAGS["EQUAL"]["HIGH"]],
    },
    JUMP_IF_ZERO_FLAG : {
        "true_flags":[FLAGS["ZERO"]["HIGH"]],
        "false_flags":[FLAGS["ZERO"]["LOW"]],
    },
    JUMP_IF_NOT_ZERO_FLAG : {
        "true_flags":[FLAGS["ZERO"]["LOW"]],
        "false_flags":[FLAGS["ZERO"]["HIGH"]],
    },
}


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the JUMP_IF_<FLAG> and
    JUMP_IF_NOT_<FLAG> operations.

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
    Generate microcode for the JUMP_IF_<FLAG> and
    JUMP_IF_NOT_<FLAG> operations.

    Returns:
        list(DataTemplate): DataTemplates for all the
        JUMP_IF_<FLAG> and JUMP_IF_NOT_<FLAG> microcode.
    """

    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:
        microcode_defs = []

        # If true, do the jump
        true_step_0_flags = _OPERATION_TO_FLAGS[signature[0]]["true_flags"]
        true_step_0_module_controls = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["PC"]["IN"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": 0,
            "flags": true_step_0_flags,
            "module_controls": true_step_0_module_controls,
        })

        # If false, don't jump
        false_step_0_flags = _OPERATION_TO_FLAGS[signature[0]]["false_flags"]
        false_step_0_module_controls = [
            MODULE_CONTROL["PC"]["COUNT"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": 0,
            "flags": false_step_0_flags,
            "module_controls": false_step_0_module_controls,
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
        // JUMP_IF_NEGATIVE_FLAG
        ////////////////////////////////////////////////////////////////

    &jinf_0
        SET ACC #10
        SUB #20
        JUMP_IF_NEGATIVE_FLAG &jinf_1
        HALT

    &jinf_1
        SET ACC #222
        SUB #5
        JUMP_IF_NEGATIVE_FLAG &jinf_halt_0
        JUMP &jinnf_0

    &jinf_halt_0
        HALT

        ////////////////////////////////////////////////////////////////
        // JUMP_IF_NOT_NEGATIVE_FLAG
        ////////////////////////////////////////////////////////////////

    &jinnf_0
        SET ACC #10
        SUB #5
        JUMP_IF_NOT_NEGATIVE_FLAG &jinnf_1
        HALT

    &jinnf_1
        SET ACC #5
        SUB #10
        JUMP_IF_NOT_NEGATIVE_FLAG &jinnf_halt_0
        JUMP &jic_0

    &jinnf_halt_0
        HALT

        ////////////////////////////////////////////////////////////////
        // JUMP_IF_CARRY
        ////////////////////////////////////////////////////////////////

    &jic_0
        SET ACC #0xFFFF
        ADD #1
        JUMP_IF_CARRY &jic_1
        HALT

    &jic_1
        SET ACC #5
        ADD #10
        JUMP_IF_CARRY &jic_halt_0
        JUMP &jinc_0

    &jic_halt_0
        HALT

        ////////////////////////////////////////////////////////////////
        // JUMP_IF_NOT_CARRY
        ////////////////////////////////////////////////////////////////

    &jinc_0
        SET ACC #18
        ADD #5
        JUMP_IF_NOT_CARRY &jinc_1
        HALT

    &jinc_1
        SET ACC #0xFFFF
        ADD #55
        JUMP_IF_NOT_CARRY &jinc_halt_0
        JUMP &jib_0

    &jinc_halt_0
        HALT

        ////////////////////////////////////////////////////////////////
        // JUMP_IF_BORROW
        ////////////////////////////////////////////////////////////////

    &jib_0
        SET ACC #0x25
        SUB #54
        JUMP_IF_BORROW &jib_1
        HALT

    &jib_1
        SET ACC #5
        ADD #10
        JUMP_IF_BORROW &jib_halt_0
        JUMP &jinb_0

    &jib_halt_0
        HALT

        ////////////////////////////////////////////////////////////////
        // JUMP_IF_NOT_BORROW
        ////////////////////////////////////////////////////////////////

    &jinb_0
        SET ACC #18
        SUB #5
        JUMP_IF_NOT_BORROW &jinb_1
        HALT

    &jinb_1
        SET ACC #0
        SUB #55
        JUMP_IF_NOT_BORROW &jinb_halt_0
        JUMP &jief_0

    &jinb_halt_0
        HALT

        ////////////////////////////////////////////////////////////////
        // JUMP_IF_EQUAL_FLAG
        ////////////////////////////////////////////////////////////////

    &jief_0
        // See the note on the ALU module because this is a bit magic.
        SET ACC #1
        SUB #2
        JUMP_IF_EQUAL_FLAG &jief_1
        HALT

    &jief_1
        SET ACC #5
        ADD #10
        JUMP_IF_EQUAL_FLAG &jief_halt_0
        JUMP &jinef_0

    &jief_halt_0
        HALT

        ////////////////////////////////////////////////////////////////
        // JUMP_IF_NOT_EQUAL_FLAG
        ////////////////////////////////////////////////////////////////

    &jinef_0
        SET ACC #34
        ADD #5
        JUMP_IF_NOT_EQUAL_FLAG &jinef_1
        HALT

    &jinef_1
        // See the note on the ALU module because this is a bit magic.
        SET ACC #1
        SUB #2
        JUMP_IF_NOT_EQUAL_FLAG &jinef_halt_0
        JUMP &jizf_0

    &jinef_halt_0
        HALT

        ////////////////////////////////////////////////////////////////
        // JUMP_IF_ZERO_FLAG
        ////////////////////////////////////////////////////////////////

    &jizf_0
        SET ACC #0
        ADD #0
        JUMP_IF_ZERO_FLAG &jizf_1
        HALT

    &jizf_1
        SET ACC #1
        ADD #1
        JUMP_IF_ZERO_FLAG &jizf_halt_0
        JUMP &jinzf_0

    &jizf_halt_0
        HALT

        ////////////////////////////////////////////////////////////////
        // JUMP_IF_NOT_ZERO_FLAG
        ////////////////////////////////////////////////////////////////

    &jinzf_0
        SET ACC #1
        ADD #1
        JUMP_IF_NOT_ZERO_FLAG &jinzf_1
        HALT

    &jinzf_1
        SET ACC #0
        ADD #0
        JUMP_IF_NOT_ZERO_FLAG &jinzf_halt_0
        JUMP &call_0

    &jinzf_halt_0
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

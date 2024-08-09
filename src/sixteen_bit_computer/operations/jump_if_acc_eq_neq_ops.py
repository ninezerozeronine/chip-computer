"""
The JUMP_IF_ACC_EQ and JUMP_IF_ACC_NEQ operations.

Jumps to a location in memory if the given module or constant
is or isn't equal to the Accumulator
"""

import textwrap

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    JUMP_IF_ACC_EQ,
    JUMP_IF_ACC_NEQ,
    A,
    B,
    C,
    CONST,
    M_CONST,
    component_to_assembly,
)
from ..language_defs import (
    MODULE_CONTROL,
    FLAGS,
    ALU_CONTROL_FLAGS,
)
from . import utils

_SUPPORTED_SIGNATURES = (
    (JUMP_IF_ACC_EQ, A, CONST),
    (JUMP_IF_ACC_EQ, B, CONST),
    (JUMP_IF_ACC_EQ, C, CONST),
    (JUMP_IF_ACC_EQ, CONST, CONST),
    (JUMP_IF_ACC_EQ, M_CONST, CONST),
    (JUMP_IF_ACC_NEQ, A, CONST),
    (JUMP_IF_ACC_NEQ, B, CONST),
    (JUMP_IF_ACC_NEQ, C, CONST),
    (JUMP_IF_ACC_NEQ, CONST, CONST),
    (JUMP_IF_ACC_NEQ, M_CONST, CONST),
)


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the JUMP_IF_ACC_(N)EQ operations.

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

    if signature[1] in (A,B,C):
        return [
            Word(value=get_instruction_index(signature)),
            Word(const_token=const_tokens[0]),
        ]
    elif signature[1] == CONST:
        return [
            Word(value=get_instruction_index(signature)),
            Word(const_token=const_tokens[0]),
            Word(const_token=const_tokens[1]),
        ]
    elif signature[1] == M_CONST:
        return [
            Word(value=get_instruction_index(signature)),
            Word(const_token=const_tokens[1]),
            Word(const_token=const_tokens[0]),
        ]


def generate_microcode_templates():
    """
    Generate microcode for the JUMP_IF_ACC_(N)EQ operations.

    Returns:
        list(DataTemplate): DataTemplates for all the JUMP_IF_ACC_(N)EQ microcode.
    """

    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:

        if signature[1] in (A,B,C):
            data_templates.extend(compare_to_module_templates(signature))
        if signature[1] == CONST:
            data_templates.extend(compare_to_const_templates(signature))
        elif signature[1] == M_CONST:
            data_templates.extend(compare_to_m_const_templates(signature))

    return data_templates


def compare_to_module_templates(signature):
    """
    E.g. E.g. JUMP_IF_ACC_(N)EQ A #DEST
    """
    microcode_defs = []

    # First unconditional step to generate flags
    step_0_flags = [FLAGS["ANY"]]
    step_0_module_controls = [
        MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
        MODULE_CONTROL["ALU"]["STORE_FLAGS"],
    ]
    step_0_module_controls.extend(ALU_CONTROL_FLAGS["COMPARE_LTE_GT_EQ"])
    microcode_defs.append({
        "step": 0,
        "flags": step_0_flags,
        "module_controls": step_0_module_controls,
    })

    # If true, do the jump
    if signature[0] == JUMP_IF_ACC_EQ:
        true_step_1_flags = [FLAGS["EQUAL"]["HIGH"]]
    else:
        true_step_1_flags = [FLAGS["EQUAL"]["LOW"]]
    true_step_1_module_controls = [
        MODULE_CONTROL["MEM"]["READ_FROM"],
        MODULE_CONTROL["PC"]["IN"],
        MODULE_CONTROL["CU"]["STEP_RESET"],
    ]
    microcode_defs.append({
        "step": 1,
        "flags": true_step_1_flags,
        "module_controls": true_step_1_module_controls,
    })

    # If false, don't do the jump
    if signature[0] == JUMP_IF_ACC_EQ:
        false_step_1_flags = [FLAGS["EQUAL"]["LOW"]]
    else:
        false_step_1_flags = [FLAGS["EQUAL"]["HIGH"]]
    false_step_1_module_controls = [
        MODULE_CONTROL["PC"]["COUNT"],
        MODULE_CONTROL["CU"]["STEP_RESET"],
    ]
    microcode_defs.append({
        "step": 1,
        "flags": false_step_1_flags,
        "module_controls": false_step_1_module_controls,
    })

    instr_index = get_instruction_index(signature)
    data_templates = utils.assemble_explicit_instruction_steps(
        instr_index, microcode_defs
    )

    return data_templates


def compare_to_const_templates(signature):
    """
    E.g. JUMP_IF_ACC_(N)EQ #VAL #DEST
    """
    microcode_defs = []

    # First Unconditional step to actually generate the flags
    step_0_flags = [FLAGS["ANY"]]
    step_0_module_controls = [
        MODULE_CONTROL["MEM"]["READ_FROM"],
        MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        MODULE_CONTROL["PC"]["COUNT"],
        MODULE_CONTROL["MAR"]["COUNT"],
    ]
    step_0_module_controls.extend(ALU_CONTROL_FLAGS["COMPARE_LTE_GT_EQ"])
    microcode_defs.append({
        "step": 0,
        "flags": step_0_flags,
        "module_controls": step_0_module_controls,
    })

    # If true, do the jump
    if signature[0] == JUMP_IF_ACC_EQ:
        true_step_1_flags = [FLAGS["EQUAL"]["HIGH"]]
    else:
        true_step_1_flags = [FLAGS["EQUAL"]["LOW"]]
    true_step_1_module_controls = [
        MODULE_CONTROL["MEM"]["READ_FROM"],
        MODULE_CONTROL["PC"]["IN"],
        MODULE_CONTROL["CU"]["STEP_RESET"],
    ]
    microcode_defs.append({
        "step": 1,
        "flags": true_step_1_flags,
        "module_controls": true_step_1_module_controls,
    })

    # If false, don't do the jump
    if signature[0] == JUMP_IF_ACC_EQ:
        false_step_1_flags = [FLAGS["EQUAL"]["LOW"]]
    else:
        false_step_1_flags = [FLAGS["EQUAL"]["HIGH"]]
    false_step_1_module_controls = [
        MODULE_CONTROL["PC"]["COUNT"],
        MODULE_CONTROL["CU"]["STEP_RESET"],
    ]
    microcode_defs.append({
        "step": 1,
        "flags": false_step_1_flags,
        "module_controls": false_step_1_module_controls,
    })

    instr_index = get_instruction_index(signature)
    data_templates = utils.assemble_explicit_instruction_steps(
        instr_index, microcode_defs
    )

    return data_templates


def compare_to_m_const_templates(signature):
    """
    E.g. JUMP_IF_ACC_(N)EQ [#LOC] #DEST
    """
    microcode_defs = []

    # First unconditional step to store the value to jump to 
    step_0_flags = [FLAGS["ANY"]]
    step_0_module_controls = [
        MODULE_CONTROL["MEM"]["READ_FROM"],
        MODULE_CONTROL["SHR"]["IN"],
        MODULE_CONTROL["PC"]["COUNT"],
        MODULE_CONTROL["MAR"]["COUNT"],
    ]
    microcode_defs.append({
        "step": 0,
        "flags": step_0_flags,
        "module_controls": step_0_module_controls,
    })

    # Second unconditional step to address the value to compare
    step_1_flags = [FLAGS["ANY"]]
    step_1_module_controls = [
        MODULE_CONTROL["MEM"]["READ_FROM"],
        MODULE_CONTROL["MAR"]["IN"],
        MODULE_CONTROL["PC"]["COUNT"],
    ]
    microcode_defs.append({
        "step": 1,
        "flags": step_1_flags,
        "module_controls": step_1_module_controls,
    })

    # Third unconditional step to generate the flags comparing the
    # value from memory
    step_2_flags = [FLAGS["ANY"]]
    step_2_module_controls = [
        MODULE_CONTROL["MEM"]["READ_FROM"],
        MODULE_CONTROL["ALU"]["STORE_FLAGS"],
    ]
    step_2_module_controls.extend((ALU_CONTROL_FLAGS["COMPARE_LTE_GT_EQ"]))
    microcode_defs.append({
        "step": 2,
        "flags": step_2_flags,
        "module_controls": step_2_module_controls,
    })

    # If true, do the jump
    if signature[0] == JUMP_IF_ACC_EQ:
        true_step_3_flags = [FLAGS["EQUAL"]["HIGH"]]
    else:
        true_step_3_flags = [FLAGS["EQUAL"]["LOW"]]
    true_step_3_module_controls = [
        MODULE_CONTROL["SHR"]["OUT"],
        MODULE_CONTROL["PC"]["IN"],
        MODULE_CONTROL["CU"]["STEP_RESET"],
    ]
    microcode_defs.append({
        "step": 3,
        "flags": true_step_3_flags,
        "module_controls": true_step_3_module_controls,
    })

    # If false, don't do the jump
    if signature[0] == JUMP_IF_ACC_EQ:
        false_step_3_flags = [FLAGS["EQUAL"]["LOW"]]
    else:
        false_step_3_flags = [FLAGS["EQUAL"]["HIGH"]]
    false_step_3_module_controls = [
        MODULE_CONTROL["CU"]["STEP_RESET"],
    ]
    microcode_defs.append({
        "step": 3,
        "flags": false_step_3_flags,
        "module_controls": false_step_3_module_controls,
    })

    instr_index = get_instruction_index(signature)
    data_templates = utils.assemble_explicit_instruction_steps(
        instr_index, microcode_defs
    )

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
        // JUMP_IF_ACC_EQ
        ////////////////////////////////////////////////////////////////

    &jiae_0
        SET ACC #123
        SET A #123
        JUMP_IF_ACC_EQ A &jiae_1
        HALT

    &jiae_1
        SET ACC #456
        SET B #456
        JUMP_IF_ACC_EQ B &jiae_2
        HALT

    &jiae_2
        SET ACC #789
        SET C #789
        JUMP_IF_ACC_EQ C &jiae_3
        HALT

    &jiae_3
        SET ACC #60123
        JUMP_IF_ACC_EQ #60123 &jiae_4
        HALT

    $v_jiae_0 #37
    &jiae_4
        SET ACC #37
        JUMP_IF_ACC_EQ [$v_jiae_0] &jiae_5
        HALT

    &jiae_5
        SET ACC #123
        SET A #345
        JUMP_IF_ACC_EQ A &jiae_halt_0
        
        SET ACC #456
        SET B #11111
        JUMP_IF_ACC_EQ B &jiae_halt_1

        SET ACC #789
        SET C #477
        JUMP_IF_ACC_EQ C &jiae_halt_2

        SET ACC #1011
        JUMP_IF_ACC_EQ #999 &jiae_halt_3
        JUMP &jiae_6
    
    $v_jiae_1 #37
    &jiae_6
        SET ACC #60123
        JUMP_IF_ACC_EQ [$v_jiae_1] &jiae_halt_4

        JUMP &jiane_0

    &jiae_halt_0
        NOOP
        NOOP
        HALT
        NOOP
        NOOP
    &jiae_halt_1
        NOOP
        NOOP
        HALT
        NOOP
        NOOP
    &jiae_halt_2
        NOOP
        NOOP
        HALT
        NOOP
        NOOP
    &jiae_halt_3
        NOOP
        NOOP
        HALT
        NOOP
        NOOP
    &jiae_halt_4
        NOOP
        NOOP
        HALT
        NOOP
        NOOP

        ////////////////////////////////////////////////////////////////
        // JUMP_IF_ACC_NEQ
        ////////////////////////////////////////////////////////////////

    &jiane_0
        SET ACC #123
        SET A #1234
        JUMP_IF_ACC_NEQ A &jiane_1
        HALT

    &jiane_1
        SET ACC #321
        SET B #55555
        JUMP_IF_ACC_NEQ B &jiane_2
        HALT

    &jiane_2
        SET ACC #21454
        SET C #6874
        JUMP_IF_ACC_NEQ C &jiane_3
        HALT

    &jiane_3
        SET ACC #34
        JUMP_IF_ACC_NEQ #0xFFFF &jiane_4
        HALT

    $v_jiane_0 #12345
    &jiane_4
        SET ACC #48143
        JUMP_IF_ACC_NEQ [$v_jiane_0] &jiane_5
        HALT

    &jiane_5
        SET ACC #456
        SET A #456
        JUMP_IF_ACC_NEQ A &jiane_halt_0

        SET ACC #1122
        SET B #1122
        JUMP_IF_ACC_NEQ B &jiane_halt_1

        SET ACC #3333
        SET C #3333
        JUMP_IF_ACC_NEQ C &jiane_halt_2

        SET ACC #3345
        JUMP_IF_ACC_NEQ #3345 &jiane_halt_3
        JUMP &jiane_6

    $v_jiane_1 #12345
    &jiane_6
        SET ACC #12345
        JUMP_IF_ACC_NEQ [$v_jiane_1] &jiane_halt_4
        
        JUMP &jiane_done

    &jiane_halt_0
        NOOP
        NOOP
        HALT
        NOOP
        NOOP
    &jiane_halt_1
        NOOP
        NOOP
        HALT
        NOOP
        NOOP
    &jiane_halt_2
        NOOP
        NOOP
        HALT
        NOOP
        NOOP
    &jiane_halt_3
        NOOP
        NOOP
        HALT
        NOOP
        NOOP
    &jiane_halt_4
        NOOP
        NOOP
        HALT
        NOOP
        NOOP

    &jiane_done
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
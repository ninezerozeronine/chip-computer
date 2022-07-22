"""
The JUMP_IF_ACC_<CMP> comparison operations.

<CMP> can be LT (less than), LTE (less than or equal to), GTE
(greater than or equal to), or GT (greater than).

Jumps to a location in memory based on the result of the 
comparison between the given module or constant and ACC.
"""



# 1001     SET ACC #2                  | 1053 0x041D -                   109 0x006D
#                                      | 1054 0x041E -                     2 0x0002 #2
# 1002     JUMP_IF_ACC_LT A &jialt_1   | 1055 0x041F -                   132 0x0084
#                                      | 1056 0x0420 -                  1058 0x0422 &jialt_1
# 1003     HALT                        | 1057 0x0421 -                   186 0x00BA
# 1004                                 |
# 1005 &jialt_1                        |
# 1006     SET B #123                  | 1058 0x0422 - &jialt_1          111 0x006

# At 1057 instead of halting this jumped to 186





from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    JUMP_IF_ACC_LT,
    JUMP_IF_ACC_LTE,
    JUMP_IF_ACC_GTE,
    JUMP_IF_ACC_GT,
    A,
    B,
    C,
    SP,
    CONST
)
from .. import number_utils
from ..language_defs import (
    MODULE_CONTROL,
    FLAGS,
    ALU_CONTROL_FLAGS,
)
from . import utils

_SUPPORTED_SIGNATURES = (
    (JUMP_IF_ACC_LT, A, CONST),
    (JUMP_IF_ACC_LT, B, CONST),
    (JUMP_IF_ACC_LT, C, CONST),
    (JUMP_IF_ACC_LT, SP, CONST),
    (JUMP_IF_ACC_LT, CONST, CONST),
    (JUMP_IF_ACC_LTE, A, CONST),
    (JUMP_IF_ACC_LTE, B, CONST),
    (JUMP_IF_ACC_LTE, C, CONST),
    (JUMP_IF_ACC_LTE, SP, CONST),
    (JUMP_IF_ACC_LTE, CONST, CONST),
    (JUMP_IF_ACC_GTE, A, CONST),
    (JUMP_IF_ACC_GTE, B, CONST),
    (JUMP_IF_ACC_GTE, C, CONST),
    (JUMP_IF_ACC_GTE, SP, CONST),
    (JUMP_IF_ACC_GTE, CONST, CONST),
    (JUMP_IF_ACC_GT, A, CONST),
    (JUMP_IF_ACC_GT, B, CONST),
    (JUMP_IF_ACC_GT, C, CONST),
    (JUMP_IF_ACC_GT, SP, CONST),
    (JUMP_IF_ACC_GT, CONST, CONST),
)

CONTROLS_MAP = {
    JUMP_IF_ACC_LT : {
        "gen_flags_controls": ALU_CONTROL_FLAGS["COMPARE_LT_GTE"],
        "true_flags": [FLAGS["CARRY_BORROW"]["LOW"]],
        "false_flags": [FLAGS["CARRY_BORROW"]["HIGH"]],
    },
    JUMP_IF_ACC_LTE : {
        "gen_flags_controls": ALU_CONTROL_FLAGS["COMPARE_LTE_GT_EQ"],
        "true_flags": [FLAGS["CARRY_BORROW"]["LOW"]],
        "false_flags": [FLAGS["CARRY_BORROW"]["HIGH"]],
    },
    JUMP_IF_ACC_GTE : {
        "gen_flags_controls": ALU_CONTROL_FLAGS["COMPARE_LT_GTE"],
        "true_flags": [FLAGS["CARRY_BORROW"]["HIGH"]],
        "false_flags": [FLAGS["CARRY_BORROW"]["LOW"]],
    },
    JUMP_IF_ACC_GT : {
        "gen_flags_controls": ALU_CONTROL_FLAGS["COMPARE_LTE_GT_EQ"],
        "true_flags": [FLAGS["CARRY_BORROW"]["HIGH"]],
        "false_flags": [FLAGS["CARRY_BORROW"]["LOW"]],
    },
}


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the JUMP_IF_ACC_<CMP> operations.

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

    if signature[1] == CONST:
        return [
            Word(value=get_instruction_index(signature)),
            Word(const_token=const_tokens[0]),
            Word(const_token=const_tokens[1]),
        ]
    else:
        return [
            Word(value=get_instruction_index(signature)),
            Word(const_token=const_tokens[0]),
        ]


def generate_microcode_templates():
    """
    Generate microcode for the JUMP_IF_ACC_<CMP> operations.

    Returns:
        list(DataTemplate): DataTemplates for all the JUMP_IF_ACC_<CMP> microcode.
    """

    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:
        data_templates.extend(generate_templates_for_signature(signature))

    return data_templates


def generate_templates_for_signature(signature):
    """

    Args:
        signature (Tuple(:mod:`Instruction component<.instruction_components>`)):
            The signature to generate templates for.
    Returns:
        list(DataTemplate): DataTemplates for the given signature.

    """
    microcode_defs = []

    # Comparing to a constant value, e.g.
    # JUMP_IF_ACC_<CMP> #34 &label
    if signature[1] == CONST:
        # First unconditional step to put PC into MAR
        step_0_flags = [FLAGS["ANY"]]
        step_0_module_controls = [
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
        ]
        microcode_defs.append({
            "step": 0,
            "flags": step_0_flags,
            "module_controls": step_0_module_controls,
        })

        # Second Unconditional step to actually generate the flags,
        # comparing the value from memory
        step_1_flags = [FLAGS["ANY"]]
        step_1_module_controls = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
            MODULE_CONTROL["PC"]["COUNT"],
        ]
        step_1_module_controls.extend(CONTROLS_MAP[signature[0]]["gen_flags_controls"])
        microcode_defs.append({
            "step": 1,
            "flags": step_1_flags,
            "module_controls": step_1_module_controls,
        })

        # If flag is the true condition, comparison is true, do the jump
        true_step_2_flags = CONTROLS_MAP[signature[0]]["true_flags"]
        true_step_2_module_controls = [
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
        ]
        microcode_defs.append({
            "step": 2,
            "flags": true_step_2_flags,
            "module_controls": true_step_2_module_controls,
        })

        true_step_3_flags = [FLAGS["ANY"]]
        true_step_3_module_controls = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["PC"]["IN"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": 3,
            "flags": true_step_3_flags,
            "module_controls": true_step_3_module_controls,
        })

        # If flag is the false condition, comparison is fasle, do not do the jump
        false_step_2_flags = CONTROLS_MAP[signature[0]]["false_flags"]
        false_step_2_module_controls = [
            MODULE_CONTROL["PC"]["COUNT"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": 2,
            "flags": false_step_2_flags,
            "module_controls": false_step_2_module_controls,
        })

    # Comparing to a module, e.g.
    # JUMP_IF_ACC_<CMP> B &label
    else:
        # Unconditional step to generate the flags.
        step_0_flags = [FLAGS["ANY"]]
        step_0_module_controls = [
            MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        ]
        step_0_module_controls.extend(CONTROLS_MAP[signature[0]]["gen_flags_controls"])
        microcode_defs.append({
            "step": 0,
            "flags": step_0_flags,
            "module_controls": step_0_module_controls,
        })

        # If flag is the true condition, comparison is true, do the jump
        true_step_1_flags = CONTROLS_MAP[signature[0]]["true_flags"]
        true_step_1_module_controls = [
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
        ]
        microcode_defs.append({
            "step": 1,
            "flags": true_step_1_flags,
            "module_controls": true_step_1_module_controls,
        })

        true_step_2_flags = [FLAGS["ANY"]]
        true_step_2_module_controls = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["PC"]["IN"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": 2,
            "flags": true_step_2_flags,
            "module_controls": true_step_2_module_controls,
        })

        # If flag is the false condition, comparison is fasle, do not do the jump
        false_step_1_flags = CONTROLS_MAP[signature[0]]["false_flags"]
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

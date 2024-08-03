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

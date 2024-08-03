"""
The STORE_(INCR/DECR) Operations.

These operations will take the value in ACC, store it in memory at A,
then increment or decrement the value in memory at B

It's useful for filling the screen with a colour quickly
"""

import textwrap

from ..instruction_listings import get_instruction_index
from ..instruction_components import (
    STORE_INCR,
    STORE_DECR,
    ACC,
    CONST,
    M_A,
    M_B,
    memory_ref_to_component,
    component_to_assembly,
)
from .. import number_utils
from . import utils
from ..data_structures import Word
from ..language_defs import (
    FLAGS,
    MODULE_CONTROL,
    ALU_CONTROL_FLAGS,
)

# Don't have enough instruction steps to implement
# a (STORE_INCR, CONST, M_CONST, M_CONST) :(
_SUPPORTED_SIGNATURES = (
    (STORE_INCR, ACC, M_A, M_B),
    (STORE_INCR, CONST, M_A, M_B),
    (STORE_DECR, ACC, M_A, M_B),
    (STORE_DECR, CONST, M_A, M_B),
)

def generate_machinecode(signature, const_tokens):
    if signature not in _SUPPORTED_SIGNATURES:
        raise ValueError

    if signature[1] == CONST:
        return [
            Word(value=get_instruction_index(signature)),
            Word(const_token=const_tokens[0]),
        ]
    else:
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
        control_steps = _generate_control_steps(signature)
        templates = utils.assemble_instruction_steps(
            instr_index_bitdef, flags_bitdefs, control_steps
        )
        microcode_templates.extend(templates)
    return microcode_templates


def _generate_control_steps(signature):
    if signature[1] != CONST:
        store_mod = utils.component_to_module_name(
            memory_ref_to_component(signature[2])
        )
        store_mod_to_mar = [
            MODULE_CONTROL[store_mod]["OUT"],
            MODULE_CONTROL["MAR"]["IN"]
        ]

        val_to_mem = [
            MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
            MODULE_CONTROL["MEM"]["WRITE_TO"],
        ]

        incr_decr_mod = utils.component_to_module_name(
            memory_ref_to_component(signature[3])
        )
        incr_decr_mod_to_mar = [
            MODULE_CONTROL[incr_decr_mod]["OUT"],
            MODULE_CONTROL["MAR"]["IN"]
        ]

        incr_decr_mem_val_to_alu = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
            MODULE_CONTROL["ALU"]["A_IS_BUS"],
        ]
        if signature[0] == STORE_INCR:
            incr_decr_mem_val_to_alu.extend(ALU_CONTROL_FLAGS["A_PLUS_1"])
        elif signature[0] == STORE_DECR:
            incr_decr_mem_val_to_alu.extend(ALU_CONTROL_FLAGS["A_MINUS_1"])
        else:
            raise RuntimeError(
                "Unexpected signature {sig} in store incr/decr "
                "microcode generation".format(sig=signature)
            )

        alu_to_mem = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["MEM"]["WRITE_TO"],
        ]

        return [
            store_mod_to_mar,
            val_to_mem,
            incr_decr_mod_to_mar,
            incr_decr_mem_val_to_alu,
            alu_to_mem
        ]
    
    elif signature[1] == CONST:
        val_to_shr_mar_and_pc_count = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["SHR"]["IN"],
            MODULE_CONTROL["MAR"]["COUNT"],
            MODULE_CONTROL["PC"]["COUNT"],
        ]

        store_mod = utils.component_to_module_name(
            memory_ref_to_component(signature[2])
        )
        store_mod_to_mar = [
            MODULE_CONTROL[store_mod]["OUT"],
            MODULE_CONTROL["MAR"]["IN"]
        ]

        shr_to_mem = [
            MODULE_CONTROL["SHR"]["OUT"],
            MODULE_CONTROL["MEM"]["WRITE_TO"],
        ]

        incr_decr_mod = utils.component_to_module_name(
            memory_ref_to_component(signature[3])
        )
        incr_decr_mod_to_mar = [
            MODULE_CONTROL[incr_decr_mod]["OUT"],
            MODULE_CONTROL["MAR"]["IN"]
        ]

        incr_decr_mem_val_to_alu = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
            MODULE_CONTROL["ALU"]["A_IS_BUS"],
        ]
        if signature[0] == STORE_INCR:
            incr_decr_mem_val_to_alu.extend(ALU_CONTROL_FLAGS["A_PLUS_1"])
        elif signature[0] == STORE_DECR:
            incr_decr_mem_val_to_alu.extend(ALU_CONTROL_FLAGS["A_MINUS_1"])
        else:
            raise RuntimeError(
                "Unexpected signature {sig} in store incr/decr "
                "microcode generation".format(sig=signature)
            )

        alu_to_mem = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["MEM"]["WRITE_TO"],
        ]

        return [
            val_to_shr_mar_and_pc_count,
            store_mod_to_mar,
            shr_to_mem,
            incr_decr_mod_to_mar,
            incr_decr_mem_val_to_alu,
            alu_to_mem
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


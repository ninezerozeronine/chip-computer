"""
The INCR and DECR operations.

Increnent or decrement the given argument by 1.
"""

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
    memory_ref_to_component,
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
            step_0 = [
                    MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
                    MODULE_CONTROL["ALU"]["STORE_RESULT"],
                    MODULE_CONTROL["ALU"]["STORE_FLAGS"],
                    MODULE_CONTROL["ALU"]["A_IS_BUS"],
            ]
            if signature[0] == INCR:
                step_0.extend(ALU_CONTROL_FLAGS["A_PLUS_1"])
            elif signature[0] == DECR:
                step_0.extend(ALU_CONTROL_FLAGS["A_MINUS_1"])
            else:
                raise RuntimeError(
                    "Unexpected signature {sig} in incr/decr "
                    "microcode generation".format(sig=signature)
                )
            
            # ALU back into module
            step_1 = [
                MODULE_CONTROL["ALU"]["OUT"],
                MODULE_CONTROL[utils.component_to_module_name(signature[1])]["IN"],
            ]

            control_steps = [step_0, step_1]

            templates = utils.assemble_instruction_steps(
                instr_index_bitdef, flags_bitdefs, control_steps
            )
            data_templates.extend(templates)

        elif signature[1] == M_CONST:
            mem_into_MAR = [
                MODULE_CONTROL["MEM"]["READ_FROM"],
                MODULE_CONTROL["MAR"]["IN"],
            ]

            mem_val_pm_into_alu_pc_count = [
                MODULE_CONTROL["MEM"]["READ_FROM"],
                MODULE_CONTROL["ALU"]["STORE_RESULT"],
                MODULE_CONTROL["ALU"]["STORE_FLAGS"],
                MODULE_CONTROL["ALU"]["A_IS_BUS"],
                MODULE_CONTROL["PC"]["COUNT"],
            ]
            if signature[0] == INCR:
                step_0.extend(ALU_CONTROL_FLAGS["A_PLUS_1"])
            elif signature[0] == DECR:
                step_0.extend(ALU_CONTROL_FLAGS["A_MINUS_1"])
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
                mem_into_MAR,
                mem_val_pm_into_alu_pc_count,
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
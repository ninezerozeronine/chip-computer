"""
The CALL and RETURN operations.

CALL: Push the current program counter (i.e. the next instruction to be
executed) onto the stack, then set the program counter (i.e. jump) to
the value in the given argument (module or constant).

RETURN: Pops the top of the stack into the program counter. Expects to
be used after having arrived at a section of assembly with the CALL
operation.


"""

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    CALL,
    RETURN,
    ACC,
    A,
    B,
    C,
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
    (CALL, ACC),
    (CALL, A),
    (CALL, B),
    (CALL, C),
    (CALL, CONST),
    (RETURN,),
)


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the CALL and RETURN operations.

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

    machinecode = [
        Word(value=get_instruction_index(signature))
    ]

    for const_token in const_tokens:
        machinecode.append(Word(const_token=const_token))

    return machinecode


def generate_microcode_templates():
    """
    Generate microcode for the CALL and RETURN operations.

    Returns:
        list(DataTemplate): DataTemplates for all the CALL and RETURN
        microcode.
    """
    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:
        instr_index = get_instruction_index(signature)
        instr_index_bitdef = number_utils.number_to_bitstring(
            instr_index, bit_width=8
        )
        flags_bitdefs = [FLAGS["ANY"]]

        if signature[0] == RETURN:
            sp_into_mar = [
                MODULE_CONTROL["SP"]["OUT"],
                MODULE_CONTROL["MAR"]["IN"],
            ]

            ram_into_pc = [
                MODULE_CONTROL["MEM"]["READ_FROM"],
                MODULE_CONTROL["PC"]["IN"],
            ]

            incr_sp = [
                MODULE_CONTROL["SP"]["OUT"],
                MODULE_CONTROL["ALU"]["A_IS_BUS"],
                MODULE_CONTROL["ALU"]["STORE_RESULT"],
            ]
            incr_sp.extend(ALU_CONTROL_FLAGS["A_PLUS_1"])

            alu_into_sp = [
                MODULE_CONTROL["ALU"]["OUT"],
                MODULE_CONTROL["SP"]["IN"],
            ]

            control_steps = [
                sp_into_mar,
                ram_into_pc,
                incr_sp,
                alu_into_sp,
            ]

        elif signature[0] == CALL:
            if signature[1] == CONST:
                mem_into_shr_pc_count = [
                    MODULE_CONTROL["MEM"]["READ_FROM"],
                    MODULE_CONTROL["SHR"]["IN"],
                    MODULE_CONTROL["PC"]["COUNT"],
                ]

                sp_minus1_into_alu = [
                    MODULE_CONTROL["SP"]["OUT"],
                    MODULE_CONTROL["ALU"]["A_IS_BUS"],
                    MODULE_CONTROL["ALU"]["STORE_RESULT"],
                    MODULE_CONTROL["PC"]["COUNT"],
                ]
                sp_minus1_into_alu.extend(ALU_CONTROL_FLAGS["A_MINUS_1"])

                alu_into_mar_and_sp = [
                    MODULE_CONTROL["ALU"]["OUT"],
                    MODULE_CONTROL["SP"]["IN"],
                    MODULE_CONTROL["MAR"]["IN"],
                ]

                pc_into_mem_at_sp = [
                    MODULE_CONTROL["PC"]["OUT"],
                    MODULE_CONTROL["MEM"]["WRITE_TO"],
                ]

                shr_into_pc = [
                    MODULE_CONTROL["SHR"]["OUT"],
                    MODULE_CONTROL["PC"]["IN"],
                ]
                control_steps = [
                    mem_into_shr_pc_count,
                    sp_minus1_into_alu,
                    alu_into_mar_and_sp,
                    pc_into_mem_at_sp,
                    shr_into_pc
                ]
            else:
                sp_minus1_into_alu = [
                    MODULE_CONTROL["SP"]["OUT"],
                    MODULE_CONTROL["ALU"]["A_IS_BUS"],
                    MODULE_CONTROL["ALU"]["STORE_RESULT"],
                ]
                sp_minus1_into_alu.extend(ALU_CONTROL_FLAGS["A_MINUS_1"])

                alu_into_mar_and_sp = [
                    MODULE_CONTROL["ALU"]["OUT"],
                    MODULE_CONTROL["SP"]["IN"],
                    MODULE_CONTROL["MAR"]["IN"],
                ]

                pc_onto_stack = [
                    MODULE_CONTROL["PC"]["OUT"],
                    MODULE_CONTROL["MEM"]["WRITE_TO"],
                ]

                module_into_pc = [
                    MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
                    MODULE_CONTROL["PC"]["IN"],
                ]

                control_steps = [
                    sp_minus1_into_alu,
                    alu_into_mar_and_sp,
                    pc_onto_stack,
                    module_into_pc,
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
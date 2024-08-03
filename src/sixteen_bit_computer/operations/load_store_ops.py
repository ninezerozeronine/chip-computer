"""
The LOAD and STORE operations.

Load a value from or wtire a value to memory,
"""

import textwrap

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    LOAD,
    STORE,
    ACC,
    A,
    B,
    C,
    SP,
    M_ACC,
    M_A,
    M_B,
    M_C,
    M_SP,
    M_CONST,
    memory_ref_to_component,
    component_to_assembly,
)
from .. import number_utils
from ..language_defs import (
    MODULE_CONTROL,
    FLAGS,
)
from . import utils

_SUPPORTED_SIGNATURES = (
    (LOAD, M_ACC, A),
    (LOAD, M_ACC, B),
    (LOAD, M_ACC, C),
    (LOAD, M_A, ACC),
    (LOAD, M_A, B),
    (LOAD, M_A, C),
    (LOAD, M_B, ACC),
    (LOAD, M_B, A),
    (LOAD, M_B, C),
    (LOAD, M_C, ACC),
    (LOAD, M_C, A),
    (LOAD, M_C, B),
    (LOAD, M_SP, ACC),
    (LOAD, M_SP, A),
    (LOAD, M_SP, B),
    (LOAD, M_SP, C),
    (LOAD, M_CONST, ACC),
    (LOAD, M_CONST, A),
    (LOAD, M_CONST, B),
    (LOAD, M_CONST, C),
    (STORE, ACC, M_A),
    (STORE, ACC, M_B),
    (STORE, ACC, M_C),
    (STORE, ACC, M_SP),
    (STORE, ACC, M_CONST),
    (STORE, A, M_ACC),
    (STORE, A, M_B),
    (STORE, A, M_C),
    (STORE, A, M_SP),
    (STORE, A, M_CONST),
    (STORE, B, M_ACC),
    (STORE, B, M_A),
    (STORE, B, M_C),
    (STORE, B, M_SP),
    (STORE, B, M_CONST),
    (STORE, C, M_ACC),
    (STORE, C, M_A),
    (STORE, C, M_B),
    (STORE, C, M_SP),
    (STORE, C, M_CONST),
    (STORE, SP, M_ACC),
    (STORE, SP, M_A),
    (STORE, SP, M_B),
    (STORE, SP, M_C),
    (STORE, SP, M_CONST),
)


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the LOAD and STORE instructions.

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
    Generate microcode for the LOAD and STORE operations.

    Returns:
        list(DataTemplate): DataTemplates for all the LOAD and STORE
        microcode.
    """
    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:
        instr_index = get_instruction_index(signature)
        instr_index_bitdef = number_utils.number_to_bitstring(
            instr_index, bit_width=8
        )
        flags_bitdefs = [FLAGS["ANY"]]

        if signature[0] == LOAD:
            if signature[1] == M_CONST:
                # E.g. LOAD [#123] ACC/A/B/C
                # MAR is already pointing at the mem location holding 
                # the address to read from thanks to the fetch.
                # Read from memory into module, increment PC
                control_steps = [
                    [
                        MODULE_CONTROL["MEM"]["READ_FROM"],
                        MODULE_CONTROL["MAR"]["IN"],
                        MODULE_CONTROL["PC"]["COUNT"],
                    ],
                    [
                        MODULE_CONTROL["MEM"]["READ_FROM"],
                        MODULE_CONTROL[
                            utils.component_to_module_name(signature[2])
                        ]["IN"],
                    ]
                ]
            else:
                # E.g. LOAD [ACC/A/B/C/SP] ACC/A/B/C 
                control_steps = [
                    [
                        MODULE_CONTROL[
                            utils.component_to_module_name(
                                memory_ref_to_component(
                                    signature[1]
                                )
                            )
                        ]["OUT"],
                        MODULE_CONTROL["MAR"]["IN"],
                    ],
                    [
                        MODULE_CONTROL["MEM"]["READ_FROM"],
                        MODULE_CONTROL[
                            utils.component_to_module_name(signature[2])
                        ]["IN"],
                    ],
                ]
        elif signature[0] == STORE:
            if signature[2] == M_CONST:
                # E.g. STORE ACC/A/B/C/SP [#123]
                # MAR is already pointing at the mem location holding 
                # the address to read from thanks to the fetch.
                control_steps = [
                    [
                        MODULE_CONTROL["MEM"]["READ_FROM"],
                        MODULE_CONTROL["MAR"]["IN"],
                        MODULE_CONTROL["PC"]["COUNT"],
                    ],
                    [
                        MODULE_CONTROL["MEM"]["WRITE_TO"],
                        MODULE_CONTROL[
                            utils.component_to_module_name(signature[1])
                        ]["OUT"],
                    ]
                ]
            else:
                # E.g. STORE ACC/A/B/C [ACC/A/B/C/SP]
                control_steps = [
                    [
                        MODULE_CONTROL[
                            utils.component_to_module_name(
                                memory_ref_to_component(
                                    signature[2]
                                )
                            )
                        ]["OUT"],
                        MODULE_CONTROL["MAR"]["IN"],
                    ],
                    [
                        MODULE_CONTROL["MEM"]["WRITE_TO"],
                        MODULE_CONTROL[
                            utils.component_to_module_name(signature[1])
                        ]["OUT"],
                    ],
                ]
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
    return signature in _SUPPORTED_SIGNATURES\


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

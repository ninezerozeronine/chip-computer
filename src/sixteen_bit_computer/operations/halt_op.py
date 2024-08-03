"""
The HALT operation.

Halts execution of the computer.
"""

import textwrap

from .. import instruction_listings
from ..data_structures import Word
from ..instruction_components import HALT, component_to_assembly
from .. import number_utils
from ..language_defs import (
    MODULE_CONTROL,
    FLAGS,
)
from . import utils

_SUPPORTED_SIGNATURES = frozenset([
    (HALT,),
])


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the HALT instruction.

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
        Word(value=instruction_listings.get_instruction_index(signature))
    ]


def generate_microcode_templates():
    """
    Generate microcode for the HALT operation.

    Returns:
        list(DataTemplate): DataTemplates for all the HALT microcode.
    """
    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:
        instr_index = instruction_listings.get_instruction_index(signature)
        instr_index_bitdef = number_utils.number_to_bitstring(
            instr_index, bit_width=8
        )
        flags_bitdefs = [FLAGS["ANY"]]
        control_steps = [
            [
                MODULE_CONTROL["CLOCK"]["HALT"]
            ]
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


def gen_test_assembly():
    """
    Generate assembly code that verifies the instructions work as expected.
    """
    test_assembly = """\
        ////////////////////////////////////////////////////////////////
        // HALT
        ////////////////////////////////////////////////////////////////

    // It's hard to test a HALT!
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
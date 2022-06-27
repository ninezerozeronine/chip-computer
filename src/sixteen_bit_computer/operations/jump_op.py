"""
The JUMP operation.

Starts execution at a given location
"""

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    JUMP,
    CONST,
)
from .. import number_utils
from ..language_defs import (
    MODULE_CONTROL,
    FLAGS,
)
from . import utils

_SUPPORTED_SIGNATURES = (
    (JUMP, CONST),
)


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the JUMP instruction.

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
    Generate microcode for the JUMP operation.

    Returns:
        list(DataTemplate): DataTemplates for all the JUMP microcode.
    """
    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:
        instr_index = get_instruction_index(signature)
        instr_index_bitdef = number_utils.number_to_bitstring(
            instr_index, bit_width=8
        )
        flags_bitdefs = [FLAGS["ANY"]]
        control_steps = [
            [
                MODULE_CONTROL["PC"]["OUT"],
                MODULE_CONTROL["MAR"]["IN"],
            ],
            [
                MODULE_CONTROL["MEM"]["READ_FROM"],
                MODULE_CONTROL["PC"]["IN"],
            ],
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
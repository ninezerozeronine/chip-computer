"""
The SET_ZERO operation.

Sets the given module to zero.
"""

from .. import instruction_listings
from .. import number_utils
from . import utils
from ..data_structures import Word
from ..instruction_components import SET_ZERO, ACC, A, B, C
from ..language_defs import (
    MODULE_CONTROL,
    ALU_CONTROL_FLAGS,
    FLAGS,
)


_SUPPORTED_SIGNATURES = frozenset([
    (SET_ZERO, ACC),
    (SET_ZERO, A),
    (SET_ZERO, B),
    (SET_ZERO, C),
])
"""
The list of signatures this operation supports.

An instruction signature is a tuple of the :mod:`Instruction component
<.instruction_components>` s it's made up of.
"""


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the given SET_ZERO operation.

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
    Generate microcode for the SET_ZERO operation.

    Returns:
        list(DataTemplate): DataTemplates for all the SET_ZERO microcode.
    """
    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:
        templates = _generate_microcode_templates_for_sig(signature)
        data_templates.extend(templates)

    return data_templates


def _generate_microcode_templates_for_sig(signature):
    """
    Generate microcode for the SET_ZERO operation with the given
    signature.

    Returns:
        list(DataTemplate): DataTemplates for the particular SET_ZERO
        operation microcode.
    """
    instr_index = instruction_listings.get_instruction_index(signature)
    instr_index_bitdef = number_utils.number_to_bitstring(
        instr_index, bit_width=8
    )
    flags_bitdefs = [FLAGS["ANY"]]

    step_0 = [
        MODULE_CONTROL["ALU"]["STORE_RESULT"],
    ]
    step_0.extend(ALU_CONTROL_FLAGS["ZERO"])

    step_1 = [
        MODULE_CONTROL["ALU"]["OUT"],
        MODULE_CONTROL[utils.component_to_module_name(signature[1])]["IN"],
    ]

    control_steps = [step_0, step_1]

    return utils.assemble_instruction_steps(
        instr_index_bitdef, flags_bitdefs, control_steps
    )


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
